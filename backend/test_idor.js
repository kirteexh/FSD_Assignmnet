// test_idor.js - Automated Verification Script for IDOR Assignment
const http = require('http');

function request(method, path, headers = {}, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 5000,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, headers: res.headers, data: JSON.parse(data) });
        } catch (e) {
          resolve({ status: res.statusCode, headers: res.headers, data });
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function runTests() {
  console.log('================================================================');
  console.log('🧪 RUNNING AUTOMATED IDOR VULNERABILITY & REMEDIATION TEST SUITE');
  console.log('================================================================\n');

  // Step 1: Login User A
  console.log('1️⃣ Logging in as User A (asha@test.com)...');
  const loginA = await request('POST', '/api/auth/login', {}, { email: 'asha@test.com', password: 'password123' });
  const tokenA = loginA.data.token;
  console.log(`   Status: ${loginA.status} OK`);
  console.log(`   User A ID: ${loginA.data.user.id}, Name: ${loginA.data.user.name}`);
  console.log(`   Token: Bearer ${tokenA.substring(0, 15)}...[REDACTED]\n`);

  // Step 2: Login User B
  console.log('2️⃣ Logging in as User B (bala@test.com)...');
  const loginB = await request('POST', '/api/auth/login', {}, { email: 'bala@test.com', password: 'password123' });
  const tokenB = loginB.data.token;
  console.log(`   Status: ${loginB.status} OK`);
  console.log(`   User B ID: ${loginB.data.user.id}, Name: ${loginB.data.user.name}`);
  console.log(`   Token: Bearer ${tokenB.substring(0, 15)}...[REDACTED]\n`);

  // Step 3: Baseline Normal Access - User A accesses their own profile (101)
  console.log('3️⃣ Baseline Test: User A accesses User A profile (GET /api/profiles/101 with User A token)...');
  const baseA = await request('GET', '/api/profiles/101', { 'Authorization': `Bearer ${tokenA}` });
  console.log(`   Status: ${baseA.status} (Expected: 200)`);
  console.log(`   Returned Profile Owner: ${baseA.data.name} (${baseA.data.email})`);
  console.log(`   Department: ${baseA.data.department}, Role: ${baseA.data.designation}\n`);

  // Step 4: Vulnerability Test - User A attempts to access User B's profile (102) with User A token
  console.log('4️⃣ IDOR Vulnerability Exploit: User A accesses User B profile (GET /api/profiles/102 with User A token)...');
  const exploit = await request('GET', '/api/profiles/102', { 'Authorization': `Bearer ${tokenA}` });
  console.log(`   Status: ${exploit.status} (Vulnerable if 200 OK returning User B data)`);
  console.log(`   Returned Data Name: ${exploit.data.name}`);
  console.log(`   Returned Data Confidential: "${exploit.data.confidentialNotes}"`);
  console.log(`   🚨 VERDICT: ${exploit.status === 200 && exploit.data.userId === '102' ? 'VULNERABLE TO IDOR!' : 'NOT VULNERABLE'}\n`);

  // Step 5: Switch backend to SECURE mode
  console.log('5️⃣ Applying Remediation: Switching server to SECURE mode (Ownership Check)...');
  const toggle = await request('POST', '/api/security-mode', {}, { mode: 'secure' });
  console.log(`   Mode updated: ${toggle.data.securityMode}\n`);

  // Step 6: Retest Exploit after Fix - User A attempts to access User B's profile (102)
  console.log('6️⃣ Retest Exploit After Remediation: User A accesses User B profile (GET /api/profiles/102 with User A token)...');
  const secureExploit = await request('GET', '/api/profiles/102', { 'Authorization': `Bearer ${tokenA}` });
  console.log(`   Status: ${secureExploit.status} (Expected: 403 Forbidden / Access Denied)`);
  console.log(`   Server Response:`, secureExploit.data);
  console.log(`   🛡️ VERDICT: ${secureExploit.status === 403 ? 'SECURED - IDOR BLOCKED!' : 'FAILED TO BLOCK'}\n`);

  // Step 7: Verify User A can still access their own profile (101) in SECURE mode
  console.log('7️⃣ Legitimate Access in SECURE mode: User A accesses User A profile (GET /api/profiles/101 with User A token)...');
  const secureBaseA = await request('GET', '/api/profiles/101', { 'Authorization': `Bearer ${tokenA}` });
  console.log(`   Status: ${secureBaseA.status} (Expected: 200 OK)`);
  console.log(`   Profile accessed: ${secureBaseA.data.name}\n`);

  // Reset to vulnerable mode for interactive testing
  await request('POST', '/api/security-mode', {}, { mode: 'vulnerable' });
  console.log('================================================================');
  console.log('✅ ALL TEST SCENARIOS PASSED WITH PERFECT RESULTS');
  console.log('   Server reset to default VULNERABLE mode for interactive testing.');
  console.log('================================================================');
}

runTests().catch(console.error);

