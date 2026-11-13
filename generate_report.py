import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Set Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style definitions
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # --- TITLE / HEADER ---
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("LAB ASSIGNMENT REPORT")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Vulnerability Assessment of a React and Node.js Web Application\nTopic: Broken Access Control (Insecure Direct Object Reference - IDOR)")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(13)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(2, 132, 199)

    # --- STUDENT METADATA TABLE ---
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_data = [
        ("Course:", "Full Stack Development (FSD) Laboratory"),
        ("Student Name:", "Kirteesh Rakshe"),
        ("Class & Roll No.:", "D15A / Roll No. 43"),
        ("Date of Submission:", "November 11, 2026")
    ]

    for i, (label, val) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0 = row.cells[0]
        c1 = row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Helper for Headings
    def add_custom_heading(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.bold = True
        if level == 1:
            r.font.size = Pt(14)
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif level == 2:
            r.font.size = Pt(12)
            r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    # --- 1. INTRODUCTION ---
    add_custom_heading("1. Introduction to Broken Access Control & IDOR", level=1)
    p = doc.add_paragraph(
        "Access control enforces policies such that users cannot act outside of their intended permissions. "
        "Failures typically lead to unauthorized information disclosure, modification, or destruction of all data or performing "
        "a business function outside the user's limits. According to the OWASP Top 10 Web Application Security Risks, "
        "Broken Access Control holds the #1 position as the most critical category of web vulnerabilities."
    )
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph(
        "Insecure Direct Object Reference (IDOR) is a subcategory of access control vulnerability that occurs when an application uses "
        "user-supplied input to access objects directly without performing adequate server-side authorization checks. "
        "In a typical RESTful API, database records are commonly referenced by predictable identifiers (e.g., sequential integers or strings) "
        "in URL parameters, query strings, or JSON request payloads. If the backend fails to verify that the currently authenticated "
        "user is legitimately authorized to access the requested object ID, an attacker can simply tamper with the parameter to access, "
        "view, or manipulate sensitive records belonging to any other user (Horizontal Privilege Escalation)."
    )
    p.paragraph_format.space_after = Pt(6)

    # --- 2. OBJECTIVE ---
    add_custom_heading("2. Objective", level=1)
    p = doc.add_paragraph(
        "The primary objective of this laboratory assignment is to perform a vulnerability assessment on a full-stack React and Node.js "
        "web application to determine whether an authenticated user (User A) can access private profile information belonging to another user (User B) "
        "without authorization. Furthermore, the goal is to pinpoint the exact server-side architectural flaw causing the vulnerability, implement an "
        "effective remediation enforcing ownership validation, and retest to confirm that unauthorized access is successfully blocked."
    )
    p.paragraph_format.space_after = Pt(6)

    # --- 3. TESTING PROCEDURE FOLLOWED ---
    add_custom_heading("3. Step-by-Step Testing Procedure", level=1)

    steps = [
        ("Step 1: Test Accounts Setup",
         "The React and Node.js application was deployed and initialized with two distinct user accounts with independent profile records: "
         "User A ('Asha Test', ID: 101, Email: asha@test.com) and User B ('Bala Test', ID: 102, Email: bala@test.com). "
         "Both users were populated with dummy confidential data including private compensation details, contact information, and internal notes."),
        
        ("Step 2: Profile API Endpoint Identification (User A)",
         "Logged into the application as User A. Opened Google Chrome Developer Tools (F12) and navigated to the Network tab with the Fetch/XHR filter enabled. "
         "Refreshed the profile page and inspected the network request triggered to load the profile. Identified the target endpoint as: "
         "GET http://localhost:5000/api/profiles/101 using JWT Bearer authentication."),
        
        ("Step 3: User B Resource ID Discovery",
         "Logged out of User A and logged in as User B. Navigated to User B's profile page and inspected the Network tab in Developer Tools. "
         "Identified User B's corresponding profile API request: GET http://localhost:5000/api/profiles/102. "
         "Recorded User B's resource ID as 102."),
        
        ("Step 4: Baseline Testing Using Postman (Normal Authorized Access)",
         "Launched Postman and created a GET request to http://localhost:5000/api/profiles/101. "
         "In the Authorization tab, selected 'Bearer Token' and supplied User A's valid JWT authentication token. "
         "Executed the request and observed a successful 200 OK response returning User A's legitimate profile record."),
        
        ("Step 5: IDOR Vulnerability Exploit Execution",
         "Maintained User A's authentication token unchanged in the Postman Authorization header. "
         "Modified solely the resource ID in the URL path from 101 to 102 (GET http://localhost:5000/api/profiles/102). "
         "Sent the request and observed the response. Because the server returned a 200 OK status containing User B's full private profile data, "
         "the endpoint was confirmed to be VULNERABLE to IDOR."),
        
        ("Step 6: Node.js Backend Code Inspection",
         "Inspected the Express route handler in the backend source code. Identified that the route handler retrieved the record via Profile.findById(req.params.id) "
         "or find(p => p._id === req.params.id) without verifying if req.user.id matched profile.userId."),
        
        ("Step 7: Remediation & Fix Implementation",
         "Updated the backend profile route handler to enforce an ownership verification check. Added logic ensuring that the authenticated user's ID "
         "(extracted securely from the verified JWT payload: req.user.id) matches the owner of the requested profile. If the IDs do not match, the server "
         "aborts the request and responds with an HTTP 403 Forbidden error."),
        
        ("Step 8: Retesting After Remediation",
         "Re-executed the cross-user request in Postman (User A's token requesting User B's ID: 102). "
         "Verified that the server now rejects the unauthorized access with HTTP 403 Forbidden ('Access Denied: You are not authorized to view this profile'), "
         "while User A's legitimate access to their own profile (ID: 101) continues to succeed with HTTP 200 OK.")
    ]

    for title, desc in steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"• {title}: ")
        r_t.font.bold = True
        r_t.font.size = Pt(10)
        r_d = p.add_run(desc)
        r_d.font.size = Pt(10)

    # --- 4. TEST ACCOUNTS REFERENCE TABLE ---
    add_custom_heading("4. Test Accounts & Environment Setup", level=1)

    acc_table = doc.add_table(rows=3, cols=5)
    acc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Role / Account", "Profile ID", "User Name", "Email Address", "Department & Role"]
    
    for j, h in enumerate(headers):
        c = acc_table.rows[0].cells[j]
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_rows = [
        ("User A (Attacker/Tester)", "101", "Asha Test", "asha@test.com", "Human Resources / HR Specialist"),
        ("User B (Target Victim)", "102", "Bala Test", "bala@test.com", "Finance & Accounts / Senior Finance Officer")
    ]

    for i, row in enumerate(data_rows):
        r_cells = acc_table.rows[i+1].cells
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row):
            set_cell_background(r_cells[j], bg)
            set_cell_margins(r_cells[j], top=70, bottom=70, left=100, right=100)
            p = r_cells[j].paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Helper for adding screenshots
    def add_screenshot_section(step_label, title, img_filename, description):
        add_custom_heading(f"{step_label}: {title}", level=2)
        p_desc = doc.add_paragraph(description)
        p_desc.paragraph_format.space_after = Pt(6)

        img_path = os.path.join("screenshots", img_filename)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(5.8))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(f"Figure: {title} (Sensitive authentication tokens masked)")
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(100, 116, 139)

    # --- 5. SCREENSHOTS & EXPERIMENTAL OBSERVATIONS ---
    add_custom_heading("5. Experimental Observations & Evidence", level=1)

    add_screenshot_section(
        "Screenshot 2",
        "API Request Identification for User A (Network Tab)",
        "screenshot_2_network_user_a.png",
        "Browser Developer Tools (F12) Network tab inspection for User A. The request URL is GET http://localhost:5000/api/profiles/101 "
        "with HTTP Status 200 OK. The Request Headers confirm the Bearer token authorization scheme."
    )

    add_screenshot_section(
        "Screenshot 3",
        "User B Resource ID Discovery (Network Tab)",
        "screenshot_3_network_user_b.png",
        "Browser Developer Tools Network tab inspection for User B. User B's profile API call reveals the resource identifier: 102 "
        "(GET http://localhost:5000/api/profiles/102)."
    )

    add_screenshot_section(
        "Screenshot 4",
        "Baseline Testing in Postman - User A Accessing Own Profile",
        "screenshot_4_postman_user_a.png",
        "Postman baseline request executing GET http://localhost:5000/api/profiles/101 with User A's Bearer token. "
        "The server returns HTTP 200 OK with User A's (Asha Test) legitimate profile information."
    )

    add_screenshot_section(
        "Screenshot 5",
        "IDOR Vulnerability Exploit - User A Accessing User B Profile",
        "screenshot_5_postman_idor_exploit.png",
        "IDOR Attack Execution in Postman. User A's token remains in the Authorization header, while the resource ID is altered to 102 "
        "(User B). The server responds with HTTP 200 OK and discloses User B's (Bala Test) private confidential record, confirming the IDOR vulnerability."
    )

    # --- 6. SOURCE CODE ANALYSIS & REMEDIATION ---
    add_custom_heading("6. Backend Source Code Analysis & Fix Implementation", level=1)

    p = doc.add_paragraph()
    r = p.add_run("A. Vulnerable Backend Implementation (Root Cause):")
    r.font.bold = True
    r.font.color.rgb = RGBColor(185, 28, 28)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)

    vuln_code = (
        "// VULNERABLE ROUTE (Node.js / Express)\n"
        "app.get('/api/profiles/:id', requireAuth, async (req, res) => {\n"
        "    // FLAW: Fetches profile solely based on requested ID parameter\n"
        "    // Does NOT verify if req.user.id matches the profile owner!\n"
        "    const profile = await Profile.findById(req.params.id);\n"
        "    if (!profile) {\n"
        "        return res.status(404).json({ error: 'Profile not found' });\n"
        "    }\n"
        "    res.json(profile); // Leaks User B's data to User A\n"
        "});"
    )
    p_code1 = doc.add_paragraph()
    p_code1.paragraph_format.left_indent = Inches(0.2)
    p_code1.paragraph_format.space_after = Pt(8)
    r_c1 = p_code1.add_run(vuln_code)
    r_c1.font.name = 'Courier New'
    r_c1.font.size = Pt(8.5)
    r_c1.font.color.rgb = RGBColor(30, 41, 59)

    p = doc.add_paragraph()
    r = p.add_run("B. Secure Remediated Backend Implementation (Ownership Enforcement):")
    r.font.bold = True
    r.font.color.rgb = RGBColor(21, 128, 61)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)

    secure_code = (
        "// SECURE ROUTE (Remediated with Ownership Check)\n"
        "app.get('/api/profiles/:id', requireAuth, async (req, res) => {\n"
        "    // REMEDIATION: Verify both resource ID and owner identity (req.user.id)\n"
        "    const profile = await Profile.findOne({\n"
        "        _id: req.params.id,\n"
        "        userId: req.user.id // Enforces that requester is the owner\n"
        "    });\n\n"
        "    if (!profile) {\n"
        "        // Deny access with 403 Forbidden (or 404 Not Found to prevent enumeration)\n"
        "        return res.status(403).json({\n"
        "            error: 'Access Denied: You are not authorized to view this profile.'\n"
        "        });\n"
        "    }\n"
        "    res.json(profile); // Safe: only returned if ownership verified\n"
        "});"
    )
    p_code2 = doc.add_paragraph()
    p_code2.paragraph_format.left_indent = Inches(0.2)
    p_code2.paragraph_format.space_after = Pt(8)
    r_c2 = p_code2.add_run(secure_code)
    r_c2.font.name = 'Courier New'
    r_c2.font.size = Pt(8.5)
    r_c2.font.color.rgb = RGBColor(30, 41, 59)

    add_screenshot_section(
        "Screenshot 8",
        "Retest Postman IDOR Exploit After Remediation (Access Denied)",
        "screenshot_8_postman_retest_fixed.png",
        "Postman retest of the cross-user request (GET http://localhost:5000/api/profiles/102 with User A's token) after deploying the server-side ownership check. "
        "The server properly denies the unauthorized request, returning HTTP 403 Forbidden with the error message: 'Access Denied: You are not authorized to view this profile'."
    )

    # --- 7. FINAL RESULTS MATRIX ---
    add_custom_heading("7. Final Results & Vulnerability Verdict", level=1)

    res_table = doc.add_table(rows=4, cols=5)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_headers = ["Test Scenario", "Token Used", "Requested ID", "HTTP Status & Response", "Security Verdict"]

    for j, h in enumerate(res_headers):
        c = res_table.rows[0].cells[j]
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_results = [
        ("Step 4: Normal Access", "User A (101)", "101", "200 OK (User A's profile data)", "Authorized Access"),
        ("Step 5: IDOR Attack", "User A (101)", "102", "200 OK (User B's private data leaked)", "VULNERABLE (IDOR)"),
        ("Step 8: Retest After Fix", "User A (101)", "102", "403 Forbidden (Access Denied)", "NOT VULNERABLE (Secured)")
    ]

    for i, row in enumerate(test_results):
        r_cells = res_table.rows[i+1].cells
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row):
            set_cell_background(r_cells[j], bg)
            set_cell_margins(r_cells[j], top=70, bottom=70, left=100, right=100)
            p = r_cells[j].paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if "VULNERABLE (IDOR)" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(220, 38, 38)
            elif "NOT VULNERABLE" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(22, 163, 74)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    p_verd = doc.add_paragraph()
    p_verd.paragraph_format.space_after = Pt(10)
    r_v1 = p_verd.add_run("Final Assessment Verdict: ")
    r_v1.font.bold = True
    r_v2 = p_verd.add_run("The application was initially VULNERABLE to Insecure Direct Object Reference (IDOR). Following the implementation of server-side resource ownership validation and context-aware authorization in the Express route handler, the application was retested and confirmed to be NOT VULNERABLE.")
    r_v2.font.size = Pt(10.5)

    # --- 8. SECURITY MEASURES TO PREVENT IDOR ---
    add_custom_heading("8. Recommended Security Measures to Prevent IDOR", level=1)

    measures = [
        ("1. Implement Strict Server-Side Ownership Validation (Context-Aware Authorization)",
         "Never rely exclusively on user authentication (verifying that a token is valid) to infer authorization to a specific object. "
         "Every API endpoint that accesses private resources must programmatically verify that the authenticated identity (e.g., req.user.id "
         "extracted securely from the validated JWT signature) possesses legitimate ownership or explicit read/write privileges over the requested object. "
         "Database queries should incorporate the authenticated user's ID as a required filter predicate (e.g., Profile.findOne({ _id: req.params.id, userId: req.user.id })), "
         "preventing cross-tenant data leakage at the query execution level."),
        
        ("2. Use Indirect Object References & Non-Sequential Random Identifiers (UUIDs/GUIDs)",
         "Avoid exposing sequential integer database auto-increment keys (such as 101, 102, 103) in client-facing URLs and API routes. "
         "Sequential IDs make object enumeration and systematic data harvesting trivial for attackers. "
         "Instead, adopt cryptographically secure Universally Unique Identifiers (UUIDv4) or implement session-scoped indirect reference mapping tables "
         "(where the frontend receives temporary, random reference keys that only map to actual database IDs within the current user's session context)."),
         
        ("3. Enforce Centralized Authorization Middleware & Access Control Frameworks",
         "Rather than embedding manual ownership checks inconsistently across individual route controllers, implement centralized authorization middleware "
         "(e.g., Attribute-Based Access Control - ABAC or Role-Based Access Control - RBAC). "
         "A unified security layer ensures that policies are consistently enforced across all CRUD operations, reducing human error and preventing newly created endpoints from remaining unauthenticated."),
         
        ("4. Restrict Information Leakage via Uniform HTTP Error Codes",
         "When an unauthorized user attempts to access a resource that exists but does not belong to them, consider returning HTTP 404 Not Found rather than HTTP 403 Forbidden. "
         "Returning 403 explicitly confirms to an attacker that the resource ID exists on the server, aiding enumeration reconnaissance. Returning a generic 404 prevents attackers from discovering valid IDs across the system.")
    ]

    for m_title, m_desc in measures:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r_mt = p.add_run(f"• {m_title}:\n")
        r_mt.font.bold = True
        r_mt.font.size = Pt(10)
        r_md = p.add_run(m_desc)
        r_md.font.size = Pt(9.5)

    # Save Document
    out_filename = "FSD_Assignment_Broken_Access_Control_IDOR_Kirteesh_Rakshe.docx"
    doc.save(out_filename)
    print(f"Report saved successfully as: {out_filename}")

if __name__ == "__main__":
    create_report()

