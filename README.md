# Full Stack Development (FSD) Lab Assignment
## Vulnerability Assessment of a React and Node.js Web Application
### Topic: Broken Access Control (Insecure Direct Object Reference - IDOR)

**Student Name:** Kirteesh Rakshe  
**Class:** D15A  
**Roll No:** 43  
**Date:** November 11, 2026  

---

## 📁 Project Directory Structure
```
FSD_Assignment/
├── backend/
│   ├── public/                      # Compiled React frontend (Vite production build)
│   ├── server.js                    # Express server with vulnerable & secure routes + JWT
│   ├── test_idor.js                 # Automated CLI test suite for all IDOR scenarios
│   └── package.json                 # Backend dependencies (express, cors, jsonwebtoken, bcryptjs)
├── frontend/                        # React Frontend Source Code (Vite + React)
│   ├── src/
│   │   ├── App.jsx                  # Main Interactive Lab UI (DevTools & Postman simulator)
│   │   ├── main.jsx
│   │   └── index.css                # Dark-mode styling with security badges
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── postman/
│   ├── FSD_IDOR_Assessment.postman_collection.json    # Ready-to-import Postman Collection
│   └── FSD_IDOR_Environment.postman_environment.json # Postman Environment with {{base_url}} & tokens
├── screenshots/                     # Extracted screenshots for the report
│   ├── screenshot_2_network_user_a.png
│   ├── screenshot_3_network_user_b.png
│   ├── screenshot_4_postman_user_a.png
│   ├── screenshot_5_postman_idor_exploit.png
│   └── screenshot_8_postman_retest_fixed.png
├── Broken Access Control (IDOR).docx                 # Original Assignment Brief
├── Help Decument - Broken Access Control (IDOR).docx # Original Step-by-Step Guide
├── generate_report.py                                # Automated Word Report Generator script
├── FSD_Assignment_Broken_Access_Control_IDOR_Kirteesh_Rakshe.docx # Final Submitted Word Report
└── package.json                                      # Root helper scripts
```

---

## 🚀 Quick Start Guide

### 1. Start the Full-Stack Application
From the `FSD_Assignment` folder, run:
```bash
npm start
```
*(Or `node backend/server.js`)*

The server will start on **`http://localhost:5000`**.  
Opening `http://localhost:5000` in any web browser opens the **React Web Application** directly!

### 2. Run the Automated IDOR Verification Suite
In a separate terminal, run:
```bash
npm test
```
This executes `backend/test_idor.js` which automatically tests:
- User A & User B authentication
- User A baseline request (`GET /api/profiles/101`) $\rightarrow$ 200 OK
- User A IDOR attack on User B (`GET /api/profiles/102`) $\rightarrow$ 200 OK (Confirms **VULNERABLE**)
- Toggles backend to **SECURE** mode (ownership check)
- Retests User A IDOR attack on User B $\rightarrow$ 403 Forbidden (Confirms **NOT VULNERABLE**)

---

## 📝 Steps To Be Performed By You (Manual Testing & Evidence Capture)

Follow these steps if you want to perform the lab manually in your browser and in Postman:

### **Step 1: Open the Application & Note the Accounts**
1. Open your browser and go to: **`http://localhost:5000`**
2. Notice the two pre-seeded test accounts:
   - **User A (Asha Test):** Email `asha@test.com`, ID: `101`, Password: `password123`
   - **User B (Bala Test):** Email `bala@test.com`, ID: `102`, Password: `password123`

### **Step 2: Inspect User A's API Endpoint in Browser DevTools**
1. In the web portal, click **"User A — Asha Test"** to log in.
2. Press `F12` (or Right-Click $\rightarrow$ **Inspect**) to open **Browser Developer Tools**.
3. Go to the **Network** tab and click the **Fetch/XHR** filter.
4. Refresh the page or click "Test ID: 101".
5. Click on the **`101`** request in the list:
   - **Request URL:** `http://localhost:5000/api/profiles/101`
   - **Request Method:** `GET`
   - **Status:** `200 OK`
   - **Authorization:** `Bearer <token>` in Request Headers
6. 📸 *(Screenshot 2):* Capture the Network tab showing the URL and HTTP method (hide the raw token).

### **Step 3: Identify User B's Resource ID**
1. In the web portal, click **"User B — Bala Test"**.
2. In the DevTools **Network** tab, inspect the new profile request:
   - **Request URL:** `http://localhost:5000/api/profiles/102`
   - **Resource ID:** `102`
3. 📸 *(Screenshot 3):* Capture the Network tab showing User B's request and resource ID `102`.

### **Step 4: Test in Postman (Baseline Test)**
1. Open **Postman**.
2. Click **Import** $\rightarrow$ select `postman/FSD_IDOR_Assessment.postman_collection.json` and `postman/FSD_IDOR_Environment.postman_environment.json`.
3. In the collection, open **"1. Authentication"** $\rightarrow$ **"Login - User A (Asha Test)"** and click **Send**. (This automatically stores User A's token!).
4. Open **"Step 4: User A Accesses Own Profile (Baseline)"**:
   - Method: `GET`
   - URL: `http://localhost:5000/api/profiles/101`
   - Authorization: `Bearer Token` $\rightarrow$ User A's token
5. Click **Send** $\rightarrow$ Observe **200 OK** returning Asha Test's profile.
6. 📸 *(Screenshot 4):* Capture Postman request and response.

### **Step 5: Perform the IDOR Exploit**
1. Open **"Step 5: IDOR Exploit - User A Accesses User B Profile"**:
   - Keep User A's Bearer token unchanged!
   - Change the URL to: `http://localhost:5000/api/profiles/102`
2. Click **Send**.
3. **Observation:** The server responds with **200 OK** and reveals **User B's (Bala Test) private confidential details** (Bonus, Bank Account, Salary)!
4. **Verdict:** **VULNERABLE to IDOR**.
5. 📸 *(Screenshot 5):* Capture the Postman exploit request and response showing User B's data returned to User A.

### **Step 6 & 7: Backend Code Inspection & Remediation**
1. Inspect `backend/server.js`:
   - **Vulnerable Code:** Fetches profile using only `req.params.id` without checking if `req.user.id === profile.userId`.
   - **Secure Code:** Enforces `profile.userId === req.user.id`, returning `403 Forbidden` if unauthorized.
2. In the React portal, click the button **"Switch to 🛡️ SECURE Mode (Fix)"** at the top  
   *(or send request "Step 7: Switch Backend to SECURE Mode" in Postman)*.

### **Step 8: Retest After the Fix**
1. In Postman, open **"Step 8: Retest IDOR Attack After Fix (Blocked)"** (`GET http://localhost:5000/api/profiles/102` with User A's token).
2. Click **Send**.
3. **Observation:** Server responds with **403 Forbidden**:
   ```json
   {
     "error": "Access Denied: You are not authorized to view this profile.",
     "authenticatedUser": "101",
     "requestedResource": "102"
   }
   ```
4. Confirm User A can still access their own profile (`GET http://localhost:5000/api/profiles/101` $\rightarrow$ 200 OK).
5. **Verdict:** **NOT VULNERABLE (Secured)**.
6. 📸 *(Screenshot 8):* Capture Postman showing the 403 Forbidden response.

---

## 📄 Final Submission Report
The final report has been generated:
- File name: **`FSD_Assignment_Broken_Access_Control_IDOR_Kirteesh_Rakshe.docx`**
- It contains all required sections, student details, testing procedure, code analysis, final results table, security prevention measures, and all embedded screenshot figures.

