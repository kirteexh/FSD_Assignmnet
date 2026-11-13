import os
import base64

def get_base64_image(filename):
    path = os.path.join('screenshots', filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

img2 = get_base64_image('screenshot_2_network_user_a.png')
img3 = get_base64_image('screenshot_3_network_user_b.png')
img4 = get_base64_image('screenshot_4_postman_user_a.png')
img5 = get_base64_image('screenshot_5_postman_idor_exploit.png')
img8 = get_base64_image('screenshot_8_postman_retest_fixed.png')

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FSD Lab Assignment - Broken Access Control (IDOR) Assessment Report</title>
  <style>
    @page {
      size: A4;
      margin: 18mm;
    }
    body {
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background: #f8fafc;
      padding: 30px;
      max-width: 900px;
      margin: 0 auto;
    }
    .report-card {
      background: #ffffff;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      border: 1px solid #e2e8f0;
    }
    h1 {
      font-size: 24px;
      color: #0f172a;
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .subtitle {
      font-size: 15px;
      color: #0284c7;
      font-weight: 600;
      margin-bottom: 24px;
      border-bottom: 2px solid #0284c7;
      padding-bottom: 12px;
    }
    .meta-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 30px;
      background: #f1f5f9;
      border-radius: 6px;
      overflow: hidden;
    }
    .meta-table td {
      padding: 10px 16px;
      font-size: 14px;
      border-bottom: 1px solid #e2e8f0;
    }
    .meta-table td.label {
      font-weight: 700;
      width: 25%;
      color: #334155;
      background: #e2e8f0;
    }
    h2 {
      font-size: 18px;
      color: #0f172a;
      margin-top: 30px;
      margin-bottom: 12px;
      padding-bottom: 6px;
      border-bottom: 1px solid #cbd5e1;
    }
    h3 {
      font-size: 15px;
      color: #1e293b;
      margin-top: 20px;
      margin-bottom: 8px;
    }
    p, li {
      font-size: 14px;
      color: #334155;
      text-align: justify;
    }
    ul, ol {
      margin-left: 20px;
      margin-bottom: 16px;
    }
    li {
      margin-bottom: 6px;
    }
    .data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 13px;
    }
    .data-table th, .data-table td {
      border: 1px solid #cbd5e1;
      padding: 10px 12px;
      text-align: left;
    }
    .data-table th {
      background: #1e293b;
      color: #ffffff;
      font-weight: 600;
    }
    .data-table tr:nth-child(even) {
      background: #f8fafc;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
    }
    .badge-danger {
      background: #fee2e2;
      color: #b91c1c;
    }
    .badge-success {
      background: #dcfce7;
      color: #15803d;
    }
    .figure-container {
      margin: 20px 0;
      text-align: center;
      background: #f8fafc;
      padding: 14px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
      page-break-inside: avoid;
    }
    .figure-container img {
      max-width: 100%;
      height: auto;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .figure-caption {
      font-size: 12px;
      color: #64748b;
      font-style: italic;
      margin-top: 8px;
    }
    pre {
      background: #0f172a;
      color: #f8fafc;
      padding: 14px 18px;
      border-radius: 6px;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 12.5px;
      overflow-x: auto;
      margin: 14px 0;
      line-height: 1.45;
    }
    .verdict-box {
      padding: 16px 20px;
      border-radius: 8px;
      margin: 20px 0;
      font-size: 14px;
      border-left: 5px solid;
    }
    .verdict-box.final {
      background: #eff6ff;
      border-color: #2563eb;
      color: #1e40af;
    }
    @media print {
      body {
        padding: 0;
        background: #ffffff;
      }
      .report-card {
        padding: 0;
        box-shadow: none;
        border: none;
      }
      .figure-container {
        page-break-inside: avoid;
      }
    }
  </style>
</head>
<body>
  <div class="report-card">
    <h1>Lab Assignment Report</h1>
    <div class="subtitle">Vulnerability Assessment of a React and Node.js Web Application<br>Topic: Broken Access Control (Insecure Direct Object Reference - IDOR)</div>

    <table class="meta-table">
      <tr>
        <td class="label">Course:</td>
        <td>Full Stack Development (FSD) Laboratory</td>
      </tr>
      <tr>
        <td class="label">Student Name:</td>
        <td>Kirteesh Rakshe</td>
      </tr>
      <tr>
        <td class="label">Class & Roll No.:</td>
        <td>D15A / Roll No. 43</td>
      </tr>
      <tr>
        <td class="label">Date of Submission:</td>
        <td>November 11, 2026</td>
      </tr>
    </table>

    <h2>1. Introduction to Broken Access Control & IDOR</h2>
    <p>
      Access control enforces security policies preventing users from acting outside their designated permissions. Failures in access control can lead to unauthorized data exposure, malicious modification, account takeover, or the elevation of user privileges. According to the OWASP Top 10 Web Application Security Risks, <strong>Broken Access Control</strong> ranks as the <strong>#1 most critical web security risk</strong> worldwide.
    </p>
    <p>
      <strong>Insecure Direct Object Reference (IDOR)</strong> occurs when an application receives user-supplied input to reference database records or server-side objects directly (e.g., via primary keys, resource IDs, or predictable filenames in API endpoints) without validating whether the requesting user is authorized to interact with that object. When attackers manipulate predictable identifiers in URL parameters or request payloads to access unauthorized resources belonging to other peers, this results in <strong>Horizontal Privilege Escalation</strong>.
    </p>

    <h2>2. Objective</h2>
    <p>
      The objective of this vulnerability assessment is to test an authenticated full-stack React and Node.js web application to determine whether an authenticated user (<strong>User A</strong>) can access private profile information belonging to another user (<strong>User B</strong>) without authorization. In addition, the assignment requires analyzing the root cause within the Express route handler, implementing server-side ownership verification to remediate the vulnerability, and retesting to confirm effective access restriction.
    </p>

    <h2>3. Test Accounts & Environment Setup</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Role / Persona</th>
          <th>Resource ID</th>
          <th>Full Name</th>
          <th>Official Email</th>
          <th>Department & Role</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>User A (Attacker / Tester)</strong></td>
          <td><code>101</code></td>
          <td>Asha Test</td>
          <td>asha@test.com</td>
          <td>Human Resources / HR Specialist</td>
        </tr>
        <tr>
          <td><strong>User B (Target Victim)</strong></td>
          <td><code>102</code></td>
          <td>Bala Test</td>
          <td>bala@test.com</td>
          <td>Finance & Accounts / Senior Finance Officer</td>
        </tr>
      </tbody>
    </table>

    <h2>4. Testing Procedure Followed</h2>
    <ol>
      <li><strong>Step 1: Test Accounts Initialization:</strong> Created two test accounts (User A - Asha Test, ID: 101 and User B - Bala Test, ID: 102) with distinct profile records and sensitive internal attributes.</li>
      <li><strong>Step 2: API Endpoint Identification (User A):</strong> Logged in as User A, opened Browser Developer Tools (<code>F12</code>) &rarr; Network tab &rarr; Fetch/XHR filter, and identified the profile endpoint: <code>GET http://localhost:5000/api/profiles/101</code> using a Bearer token.</li>
      <li><strong>Step 3: User B Resource ID Discovery:</strong> Logged in as User B and captured the profile request in DevTools to record User B's resource ID (<code>102</code>).</li>
      <li><strong>Step 4: Baseline Testing in Postman:</strong> Tested <code>GET http://localhost:5000/api/profiles/101</code> with User A's Bearer token in Postman, verifying a legitimate <code>200 OK</code> response with User A's profile.</li>
      <li><strong>Step 5: IDOR Attack Execution:</strong> Kept User A's Bearer token unchanged while modifying only the resource ID from <code>101</code> to <code>102</code> (<code>GET http://localhost:5000/api/profiles/102</code>). The server returned <code>200 OK</code> with User B's confidential record, proving the IDOR vulnerability.</li>
      <li><strong>Step 6: Backend Code Inspection:</strong> Examined the Node.js Express route handler and identified the flaw: the server retrieved profiles by ID without verifying if <code>req.user.id === profile.userId</code>.</li>
      <li><strong>Step 7: Remediation & Fix:</strong> Updated the route to enforce ownership verification. If the authenticated user does not own the requested record, the server responds with <code>403 Forbidden</code>.</li>
      <li><strong>Step 8: Retesting After Fix:</strong> Re-executed the attack request in Postman. The server successfully denied cross-user access with <code>403 Forbidden</code>, while User A's own profile remained accessible.</li>
    </ol>

    <h2>5. Experimental Observations & Screenshots</h2>

    <h3>Screenshot 2: API Request Identification for User A (Network Tab)</h3>
    <p>Inspecting User A's profile retrieval request in Google Chrome Developer Tools. URL: <code>http://localhost:5000/api/profiles/101</code> with HTTP Method <code>GET</code> and Status <code>200 OK</code>.</p>
    <div class="figure-container">
      <img src="IMG2_PLACEHOLDER" alt="Screenshot 2: Network Tab User A">
      <div class="figure-caption">Figure 1: Capture of User A's profile API request in Browser DevTools Network tab (Tokens masked).</div>
    </div>

    <h3>Screenshot 3: User B Resource ID Discovery (Network Tab)</h3>
    <p>Inspecting User B's profile request to note the resource identifier: <code>102</code>.</p>
    <div class="figure-container">
      <img src="IMG3_PLACEHOLDER" alt="Screenshot 3: Network Tab User B">
      <div class="figure-caption">Figure 2: Capture of User B's profile API request displaying resource ID 102.</div>
    </div>

    <h3>Screenshot 4: Baseline Testing in Postman (User A Accessing Own Profile)</h3>
    <p>Legitimate authorized access: User A requests their own profile (<code>/api/profiles/101</code>) with their valid Bearer token. The server returns <code>200 OK</code> with Asha Test's profile.</p>
    <div class="figure-container">
      <img src="IMG4_PLACEHOLDER" alt="Screenshot 4: Postman User A">
      <div class="figure-caption">Figure 3: Postman request and response for User A baseline test (Status 200 OK).</div>
    </div>

    <h3>Screenshot 5: IDOR Vulnerability Exploit (User A Accessing User B's Profile)</h3>
    <p>The IDOR exploit: Requesting User B's resource ID (<code>102</code>) while presenting User A's token. The server responds with <code>200 OK</code> and leaks User B's confidential internal salary and bonus data.</p>
    <div class="figure-container">
      <img src="IMG5_PLACEHOLDER" alt="Screenshot 5: IDOR Exploit Postman">
      <div class="figure-caption">Figure 4: Postman IDOR exploit demonstrating cross-user private data exposure (Status 200 OK - VULNERABLE).</div>
    </div>

    <h2>6. Backend Code Inspection & Remediation</h2>
    <h3>A. Vulnerable Express Route Handler (Root Cause)</h3>
    <pre><code>// VULNERABLE ROUTE (Node.js / Express)
app.get("/api/profiles/:id", requireAuth, async (req, res) => {
  // FLAW: Retrieves profile solely by requested ID without verifying ownership!
  const profile = await Profile.findById(req.params.id);
  if (!profile) {
    return res.status(404).json({ error: "Profile not found" });
  }
  res.json(profile); // Leaks User B's private data to User A
});</code></pre>

    <h3>B. Secure Remediated Route Handler (Ownership Enforcement)</h3>
    <pre><code>// SECURE ROUTE (Remediated with Ownership Check)
app.get("/api/profiles/:id", requireAuth, async (req, res) => {
  // REMEDIATION: Verify both profile ID and owner identity (req.user.id)
  const profile = await Profile.findOne({
    _id: req.params.id,
    userId: req.user.id // Enforces that requester owns this profile
  });

  if (!profile) {
    // Return 403 Forbidden or 404 Not Found to prevent enumeration
    return res.status(403).json({
      error: "Access Denied: You are not authorized to view this profile."
    });
  }

  res.json(profile); // Authorized access only
});</code></pre>

    <h3>Screenshot 8: Retest Postman IDOR Exploit After Remediation</h3>
    <p>Retesting the cross-user exploit after deploying the ownership check. The server blocks the unauthorized request with <code>403 Forbidden</code>.</p>
    <div class="figure-container">
      <img src="IMG8_PLACEHOLDER" alt="Screenshot 8: Postman Retest Fixed">
      <div class="figure-caption">Figure 5: Postman retest after fix: server returns 403 Forbidden (NOT VULNERABLE).</div>
    </div>

    <h2>7. Final Results Matrix & Verdict</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Test Scenario</th>
          <th>Auth Token Used</th>
          <th>Target ID</th>
          <th>HTTP Status & Response</th>
          <th>Security Verdict</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Step 4: Normal Access</td>
          <td>User A (ID 101)</td>
          <td><code>101</code></td>
          <td>200 OK (User A data returned)</td>
          <td><span class="badge badge-success">Authorized Access</span></td>
        </tr>
        <tr>
          <td>Step 5: IDOR Attack</td>
          <td>User A (ID 101)</td>
          <td><code>102</code></td>
          <td>200 OK (User B private data leaked)</td>
          <td><span class="badge badge-danger">VULNERABLE (IDOR)</span></td>
        </tr>
        <tr>
          <td>Step 8: Retest After Fix</td>
          <td>User A (ID 101)</td>
          <td><code>102</code></td>
          <td>403 Forbidden (Access Denied)</td>
          <td><span class="badge badge-success">NOT VULNERABLE (Secured)</span></td>
        </tr>
      </tbody>
    </table>

    <div class="verdict-box final">
      <strong>Final Result:</strong> The web application was initially <strong>VULNERABLE</strong> to Insecure Direct Object Reference (IDOR). Following the implementation of server-side ownership verification in the Node.js Express backend, the vulnerability was remediated and confirmed to be <strong>NOT VULNERABLE</strong> upon retesting.
    </div>

    <h2>8. Security Measures to Prevent IDOR</h2>
    <ul>
      <li>
        <strong>1. Implement Strict Server-Side Ownership Validation:</strong> Never trust client-supplied resource IDs alone. Every API route handling private or tenant-specific records must verify that the authenticated subject (extracted from trusted session or JWT claims: <code>req.user.id</code>) is authorized to access the requested resource. Database queries should filter by owner: <code>Profile.findOne({ _id: req.params.id, userId: req.user.id })</code>.
      </li>
      <li>
        <strong>2. Use Non-Sequential Random Identifiers (UUIDs/GUIDs):</strong> Avoid sequential database auto-increment keys (such as 101, 102). Sequential IDs make resource enumeration trivial. Using cryptographically secure UUIDv4 or indirect session-scoped mapping tables prevents attackers from guessing other users' resource IDs.
      </li>
      <li>
        <strong>3. Deploy Centralized Authorization Middleware:</strong> Implement unified authorization middleware (RBAC / ABAC) rather than manual, ad-hoc checks in each controller to avoid human error and ensure uniform access control.
      </li>
      <li>
        <strong>4. Uniform HTTP Error Handling:</strong> Return generic HTTP 404 Not Found instead of 403 Forbidden when unauthorized access occurs, preventing attackers from confirming whether a guessed resource ID exists.
      </li>
    </ul>
  </div>
</body>
</html>
"""

html_out = template.replace('IMG2_PLACEHOLDER', img2)\
                   .replace('IMG3_PLACEHOLDER', img3)\
                   .replace('IMG4_PLACEHOLDER', img4)\
                   .replace('IMG5_PLACEHOLDER', img5)\
                   .replace('IMG8_PLACEHOLDER', img8)

with open("REPORT.html", "w", encoding="utf-8") as f:
    f.write(html_out)

print(f"Generated REPORT.html ({os.path.getsize('REPORT.html')} bytes)")
