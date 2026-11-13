const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;
const JWT_SECRET = process.env.JWT_SECRET || 'fsd_idor_lab_super_secret_jwt_key_2026';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// In-Memory Database (Pre-seeded with User A and User B as required by the assignment)
const users = [
  {
    id: '101',
    email: 'asha@test.com',
    passwordHash: bcrypt.hashSync('password123', 8),
    name: 'Asha Test',
    role: 'User'
  },
  {
    id: '102',
    email: 'bala@test.com',
    passwordHash: bcrypt.hashSync('password123', 8),
    name: 'Bala Test',
    role: 'User'
  }
];

const profiles = [
  {
    _id: '101',
    userId: '101',
    name: 'Asha Test',
    email: 'asha@test.com',
    phone: '+91 98765 43210',
    department: 'Human Resources',
    designation: 'HR Specialist',
    address: 'Flat 402, Green Valley Apartments, Mumbai, Maharashtra',
    confidentialNotes: 'User A confidential performance review: Eligible for annual increment. Performance rating 4.8/5.0.',
    accountBalance: '₹ 75,400.00',
    createdAt: '2026-01-15T09:30:00Z'
  },
  {
    _id: '102',
    userId: '102',
    name: 'Bala Test',
    email: 'bala@test.com',
    phone: '+91 91234 56789',
    department: 'Finance & Accounts',
    designation: 'Senior Finance Officer',
    address: 'Villa 14, Royal Palms, Pune, Maharashtra',
    confidentialNotes: 'CONFIDENTIAL FINANCIAL DATA: Bank A/C #987654321098, IFSC: HDFC0001234, FY26 Discretionary Bonus: ₹3,50,000.',
    accountBalance: '₹ 2,45,800.00',
    createdAt: '2026-01-20T11:15:00Z'
  }
];

// Security mode state: 'vulnerable' (default) or 'secure' (fixed)
let securityMode = 'vulnerable';

// Authentication Middleware
const requireAuth = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  if (!authHeader) {
    return res.status(401).json({
      error: 'Authentication failed: No authorization token provided'
    });
  }

  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') {
    return res.status(401).json({
      error: 'Authentication failed: Invalid Bearer token format'
    });
  }

  const token = parts[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded; // Contains { id, email, name, role }
    next();
  } catch (err) {
    return res.status(401).json({
      error: 'Authentication failed: Invalid or expired token'
    });
  }
};

// --------------------------------------------------------------------------
// AUTHENTICATION ROUTES
// --------------------------------------------------------------------------

// Login Route
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  const user = users.find(u => u.email.toLowerCase() === email.toLowerCase());
  if (!user || !bcrypt.compareSync(password, user.passwordHash)) {
    return res.status(401).json({ error: 'Invalid email or password' });
  }

  const token = jwt.sign(
    {
      id: user.id,
      email: user.email,
      name: user.name,
      role: user.role
    },
    JWT_SECRET,
    { expiresIn: '8h' }
  );

  res.json({
    message: 'Login successful',
    token,
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role
    }
  });
});

// Register Route (optional for creating additional test accounts)
app.post('/api/auth/register', (req, res) => {
  const { name, email, password, department, designation, phone } = req.body;
  if (!name || !email || !password) {
    return res.status(400).json({ error: 'Name, email, and password are required' });
  }

  if (users.find(u => u.email.toLowerCase() === email.toLowerCase())) {
    return res.status(409).json({ error: 'Email already registered' });
  }

  const newId = String(100 + users.length + 1);
  const newUser = {
    id: newId,
    email,
    passwordHash: bcrypt.hashSync(password, 8),
    name,
    role: 'User'
  };
  users.push(newUser);

  const newProfile = {
    _id: newId,
    userId: newId,
    name,
    email,
    phone: phone || '+91 90000 00000',
    department: department || 'Engineering',
    designation: designation || 'Associate Engineer',
    address: 'Sample Address, India',
    confidentialNotes: `Private record for user ${name}.`,
    accountBalance: '₹ 50,000.00',
    createdAt: new Date().toISOString()
  };
  profiles.push(newProfile);

  res.status(201).json({
    message: 'User created successfully',
    user: { id: newUser.id, name: newUser.name, email: newUser.email }
  });
});

// --------------------------------------------------------------------------
// SECURITY STATUS & TOGGLE ROUTES
// --------------------------------------------------------------------------

app.get('/api/security-status', (req, res) => {
  res.json({
    securityMode,
    description:
      securityMode === 'vulnerable'
        ? 'VULNERABLE (IDOR present: backend retrieves profile by requested ID without verifying ownership)'
        : 'SECURE (Remediated: backend enforces ownership check req.user.id === profile.userId)'
  });
});

app.post('/api/security-mode', (req, res) => {
  const { mode } = req.body;
  if (mode === 'vulnerable' || mode === 'secure') {
    securityMode = mode;
    return res.json({
      message: `Security mode successfully updated to: ${securityMode}`,
      securityMode
    });
  }
  res.status(400).json({ error: "Invalid mode. Choose 'vulnerable' or 'secure'." });
});

// --------------------------------------------------------------------------
// PROFILE ENDPOINTS (MAIN EXPERIMENT)
// --------------------------------------------------------------------------

/**
 * Standard Assignment Route: GET /api/profiles/:id
 * Switches behavior based on current securityMode
 */
app.get('/api/profiles/:id', requireAuth, (req, res) => {
  const requestedId = req.params.id;

  if (securityMode === 'vulnerable') {
    // ========================================================================
    // VULNERABLE IMPLEMENTATION (As described in Step 6 of Assignment Help Doc)
    // ========================================================================
    // Flaw: The backend retrieves the profile using req.params.id but DOES NOT
    // verify whether req.user.id equals profile.userId.
    const profile = profiles.find(p => p._id === requestedId);
    if (!profile) {
      return res.status(404).json({ error: 'Profile not found' });
    }

    // Vulnerable: Returns any profile to any authenticated user!
    return res.json(profile);
  } else {
    // ========================================================================
    // SECURE IMPLEMENTATION (As described in Step 7 of Assignment Help Doc)
    // ========================================================================
    // Fix: Perform authorization & ownership verification:
    // Only return the profile if the authenticated user owns it.
    const profile = profiles.find(
      p => p._id === requestedId && p.userId === req.user.id
    );

    if (!profile) {
      // 403 Forbidden (or 404 Not Found to prevent ID enumeration)
      return res.status(403).json({
        error: 'Access Denied: You are not authorized to view this profile.',
        authenticatedUser: req.user.id,
        requestedResource: requestedId
      });
    }

    return res.json(profile);
  }
});

// Explicit vulnerable endpoint (for testing/comparison)
app.get('/api/vulnerable/profiles/:id', requireAuth, (req, res) => {
  const profile = profiles.find(p => p._id === req.params.id);
  if (!profile) return res.status(404).json({ error: 'Profile not found' });
  res.json(profile);
});

// Explicit secure endpoint (for testing/comparison)
app.get('/api/secure/profiles/:id', requireAuth, (req, res) => {
  const profile = profiles.find(
    p => p._id === req.params.id && p.userId === req.user.id
  );
  if (!profile) {
    return res.status(403).json({
      error: 'Access Denied: Ownership verification failed.',
      authenticatedUser: req.user.id,
      requestedResource: req.params.id
    });
  }
  res.json(profile);
});

// List all registered test accounts summary (convenience helper for the UI)
app.get('/api/test-accounts', (req, res) => {
  res.json(
    users.map(u => ({
      id: u.id,
      name: u.name,
      email: u.email,
      role: u.role
    }))
  );
});

// Serve Frontend Single Page Application fallback for non-API routes (Compatible with Express 4 and Express 5)
app.use((req, res, next) => {
  if (req.method === 'GET' && !req.path.startsWith('/api')) {
    return res.sendFile(path.join(__dirname, 'public', 'index.html'));
  }
  next();
});

// Start the server
app.listen(PORT, () => {
  console.log(`======================================================`);
  console.log(`🚀 FSD IDOR Lab Server running on http://localhost:${PORT}`);
  console.log(`   Security Mode: ${securityMode.toUpperCase()}`);
  console.log(`   User A: asha@test.com (ID: 101)`);
  console.log(`   User B: bala@test.com (ID: 102)`);
  console.log(`======================================================`);
});
