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

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_page_number(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def generate_report():
    doc = docx.Document()
    
    # -------------------------------------------------------------------------
    # 1. PAGE SETUP (A4 & 1 Inch Margins)
    # -------------------------------------------------------------------------
    for section in doc.sections:
        section.page_width = Inches(8.27)   # A4 Width
        section.page_height = Inches(11.69) # A4 Height
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        # Configure Footer Page Numbering (Times New Roman, Centered, 10 pt)
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run()
        f_run.font.name = 'Times New Roman'
        f_run.font.size = Pt(10)
        f_run.font.color.rgb = RGBColor(100, 116, 139)
        add_page_number(f_run)

    # -------------------------------------------------------------------------
    # 2. GLOBAL STYLES (Times New Roman, 12 pt, 1.5 line spacing, Justified)
    # -------------------------------------------------------------------------
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(15, 23, 42)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def p(text="", bold=False, italic=False, space_after=6, space_before=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, color=RGBColor(15, 23, 42)):
        para = doc.add_paragraph()
        para.alignment = align
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_before = Pt(space_before)
        para.paragraph_format.space_after = Pt(space_after)
        if text:
            r = para.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = color
        return para

    def h1(text):
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(8)
        para.paragraph_format.keep_with_next = True
        r = para.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        return para

    def h2(text):
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_before = Pt(14)
        para.paragraph_format.space_after = Pt(6)
        para.paragraph_format.keep_with_next = True
        r = para.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 41, 59)
        return para

    def bullet(title, text):
        para = doc.add_paragraph(style='List Bullet')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_before = Pt(2)
        para.paragraph_format.space_after = Pt(4)
        r_t = para.add_run(title + ": ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        r_t.font.bold = True
        r_d = para.add_run(text)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)
        return para

    def add_figure(img_path, caption):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(12)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            r_img = p_img.add_run()
            r_img.add_picture(img_path, width=Inches(6.2))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(14)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.font.bold = True
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(71, 85, 105)

    # =========================================================================
    # COVER PAGE (Formal Engineering College Layout)
    # =========================================================================
    p("VIVEKANAND EDUCATION SOCIETY'S INSTITUTE OF TECHNOLOGY", bold=True, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    p("DEPARTMENT OF INFORMATION TECHNOLOGY", bold=True, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    p("(Affiliated to the University of Mumbai)", italic=True, space_after=36, align=WD_ALIGN_PARAGRAPH.CENTER)

    p("A MINI-PROJECT REPORT ON", bold=True, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(14)
    r_t = p_title.add_run("PHARMACARE — FULL-STACK PHARMACY MANAGEMENT SYSTEM")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(18)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(2, 132, 199)

    p("Intelligent FEFO POS Billing, Batch-Level Inventory Control, Real-Time WebSockets & Containerized DevOps Deployment", italic=True, space_after=40, align=WD_ALIGN_PARAGRAPH.CENTER)

    p("SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE DEGREE OF", bold=True, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    p("BACHELOR OF ENGINEERING IN INFORMATION TECHNOLOGY", bold=True, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    p("Under the Course of Full Stack Development (FSD) Laboratory", space_after=40, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Student & Submission Metadata Table
    sub_table = doc.add_table(rows=4, cols=2)
    sub_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sub_data = [
        ("Candidate Name:", "Kirteesh Dattatray Rakshe"),
        ("Roll Number / Class:", "Roll No. 43 / Class D15A"),
        ("Academic Year:", "2026 – 2027"),
        ("GitHub Repository:", "https://github.com/kirteexh/FSD_MiniProject")
    ]
    for i, (k, v) in enumerate(sub_data):
        row = sub_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.0)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.0
        r0 = p0.add_run(k)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r0.font.bold = True
        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.0
        r1 = p1.add_run(v)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)

    p(space_before=40, space_after=0)
    p("ACADEMIC YEAR 2026 – 2027", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    h1("TABLE OF CONTENTS")
    toc_items = [
        ("1. Introduction and Objectives", "3"),
        ("   1.1 Project Overview and Clinical Context", "3"),
        ("   1.2 Problem Statement & Industry Challenges", "3"),
        ("   1.3 Key Project Objectives", "4"),
        ("   1.4 Target Audience and User Roles", "4"),
        ("2. Technologies Used and System Design", "5"),
        ("   2.1 Technology Stack Architecture", "5"),
        ("   2.2 High-Level System Architecture Design", "6"),
        ("   2.3 Data Flow & FEFO Algorithmic Design", "7"),
        ("   2.4 Database Schema & Persistence Architecture", "8"),
        ("   2.5 RESTful API Specification and WebSocket Protocol", "9"),
        ("3. Implementation with Screenshots", "10"),
        ("   3.1 Authentication & Role-Based Access Control (RBAC)", "10"),
        ("   3.2 Intelligent FEFO POS Billing Interface", "11"),
        ("   3.3 Clinical Inventory and Batch Management", "12"),
        ("   3.4 Shelf-Life Monitoring and Expiry Protocol", "13"),
        ("   3.5 Executive Financial Analytics & Visual Reporting", "14"),
        ("4. Deployment and DevOps", "15"),
        ("   4.1 Multi-Container Docker Architecture", "15"),
        ("   4.2 Docker Compose Runtime Orchestration", "16"),
        ("   4.3 Automated CI/CD Pipeline via GitHub Actions", "17"),
        ("   4.4 Production Cloud Deployment & Security Hardening", "18"),
        ("5. Conclusion and Future Scope", "19"),
        ("   5.1 Summary of Accomplishments", "19"),
        ("   5.2 Future Enhancements & Commercial Roadmap", "19"),
        ("6. GitHub Repository & Live Deployment", "20")
    ]
    for title, page in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.line_spacing = 1.3
        p_toc.paragraph_format.space_after = Pt(3)
        r1 = p_toc.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        if not title.startswith("   "):
            r1.font.bold = True
        r2 = p_toc.add_run(f" {'·' * (65 - len(title))} {page}")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION AND OBJECTIVES
    # =========================================================================
    h1("1. Introduction and Objectives")
    
    h2("1.1 Project Overview and Clinical Context")
    p(
        "Modern pharmaceutical retail and hospital dispensaries operate in highly demanding, clinical environments where precision, "
        "speed, and regulatory compliance are essential to patient well-being and commercial sustainability. "
        "Unlike conventional commodity retail systems, pharmaceutical operations deal with potent, regulated chemical compounds, "
        "strict shelf-life expiration dates, batch traceability mandates, schedule-restricted narcotics, and dynamic manufacturer price revisions. "
        "PharmaCare is a full-stack, enterprise-grade pharmacy management web platform designed to streamline retail and hospital dispensary workflows. "
        "By combining a contemporary Next.js 14 frontend, a decoupled Express.js REST and Socket.IO backend, and dual-mode MongoDB Atlas persistence, "
        "PharmaCare modernizes traditional drug dispensing, automated batch allocation, and financial auditing."
    )

    h2("1.2 Problem Statement & Industry Challenges")
    p(
        "A comprehensive operational analysis of independent pharmacies and dispensary chains reveals several pervasive failure modes "
        "arising from legacy desktop software or manual paper-based ledger systems:"
    )
    bullet("Dead Stock & High Expiry Write-Off Losses", 
           "In conventional retail dispensaries, staff grab the most accessible medication boxes from shelves during rush hours. This human tendency leaves earlier-received batches lingering in the back of racks until they expire, generating significant recurring financial losses for pharmacy owners.")
    bullet("Slow Checkout Bottlenecks & Prescription Verification", 
           "Manual batch number entry, manual tax calculations, and disconnected verification of Schedule-H prescription drugs create prolonged queues at dispensary counters, risking patient frustration and data entry mistakes.")
    bullet("Inventory Desynchronization & Stock-Outs", 
           "Without real-time inventory synchronization, dispensaries often run out of essential, life-saving antibiotics, insulin, and cardiac formulations without advance warning.")
    bullet("Inadequate Auditing & Role Segregation", 
           "Traditional single-tier desktop systems fail to provide robust role-based access control (RBAC), leaving critical operations like stock adjustments, clinical disposal write-offs, and price updates vulnerable to untracked human error or insider theft.")

    h2("1.3 Key Project Objectives")
    p("The primary objectives established for the development of the PharmaCare platform are as follows:")
    bullet("Intelligent First-Expiry, First-Out (FEFO) POS Billing", 
           "Design and implement an automated point-of-sale checkout engine that programmatically selects and deducts inventory from the earliest expiring batch, completely eliminating human bias in dispensing aged stock.")
    bullet("Batch-Level Traceability & Clinical Audit Trails", 
           "Maintain granular lifecycle history for every individual pharmaceutical batch, including manufacturer details, manufacturing and expiry dates, purchase costs, MRP, supplier GSTINs, and audited stock adjustments.")
    bullet("Proactive Shelf-Life Expiry Monitoring", 
           "Provide real-time categorization of dispensary inventory into clinical urgency tiers (<7 days, <30 days, <90 days, and expired), complete with formal clinical write-off logging.")
    bullet("Real-Time Stock Alerts via WebSockets", 
           "Integrate bidirectional Socket.IO WebSockets to broadcast instant, asynchronous notifications to all active workstations whenever any critical medicine breaches its minimum reorder threshold.")
    bullet("Robust Role-Based Security & Production DevOps", 
           "Enforce JWT authentication with password hashing (bcryptjs) separating Store Administrator and Cashier roles, and package the complete system with Docker multi-stage containers and automated GitHub Actions CI/CD.")

    h2("1.4 Target Audience and User Roles")
    p(
        "The system explicitly caters to two distinct operational user classes with strictly partitioned permissions:"
    )
    bullet("Store Administrator (Pharmacist-in-Charge / Owner)", 
           "Authorized with comprehensive administrative privileges including medication catalog authoring, batch creation, audited stock quantity adjustments, clinical disposal approvals, purchase order procurement, staff credential provisioning, and executive financial reporting.")
    bullet("Dispensary Cashier (Sales Staff)", 
           "Authorized with frontline operational permissions focused on rapid POS barcode billing, patient prescription recording, customer invoice generation, held bill caching, and real-time stock catalog lookups.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: TECHNOLOGIES USED AND SYSTEM DESIGN
    # =========================================================================
    h1("2. Technologies Used and System Design")

    h2("2.1 Technology Stack Architecture")
    p(
        "PharmaCare leverages a modern, decoupled full-stack architecture carefully selected to achieve high concurrency, "
        "sub-second POS transaction latencies, responsive UI rendering, and production-grade reliability."
    )

    # Technology Table
    tech_table = doc.add_table(rows=5, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Architecture Tier", "Technologies & Frameworks", "Key Purpose & Justification"]
    for j, h in enumerate(t_headers):
        c = tech_table.rows[0].cells[j]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p_th = c.paragraphs[0]
        r_th = p_th.add_run(h)
        r_th.font.name = 'Times New Roman'
        r_th.font.size = Pt(11)
        r_th.font.bold = True
        r_th.font.color.rgb = RGBColor(255, 255, 255)

    tech_rows = [
        ("Frontend Presentation", 
         "Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Framer Motion, Redux Toolkit, Recharts, Lucide React", 
         "Server-Side Rendering (SSR) & Client Hydration, modular typed components, clinical dark/light theming, client-side cart state management, and real-time analytics graphs."),
        ("Backend REST & Sockets", 
         "Node.js (v18+), Express.js, TypeScript, Socket.IO, Helmet, CORS, Express-Rate-Limit, Zod, bcryptjs, JSON Web Tokens (JWT)", 
         "High-throughput asynchronous non-blocking event loop, strict RESTful API routing, bidirectional WebSocket notification broadcasting, cryptographic security, and payload schema validation."),
        ("Data Persistence", 
         "MongoDB Atlas, Mongoose ODM (Object Data Modeling), Hybrid In-Memory Fallback Engine", 
         "Document-oriented schema flexibility for multi-batch arrays, indexed geospatial/temporal querying for expiry windows, and seamless offline evaluation capability."),
        ("DevOps & Deployment", 
         "Docker, Docker Compose, Nginx Reverse Proxy, GitHub Actions CI/CD Pipeline, Render Cloud Platform", 
         "Multi-stage container image builds for minimized runtime footprint, microservice orchestration, automated testing pipelines on code push, and zero-downtime cloud hosting.")
    ]
    for i, row in enumerate(tech_rows):
        r_cells = tech_table.rows[i+1].cells
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row):
            set_cell_background(r_cells[j], bg)
            set_cell_margins(r_cells[j], top=70, bottom=70, left=100, right=100)
            p_tc = r_cells[j].paragraphs[0]
            p_tc.paragraph_format.line_spacing = 1.2
            r_tc = p_tc.add_run(val)
            r_tc.font.name = 'Times New Roman'
            r_tc.font.size = Pt(10.5)

    p(space_after=8)

    h2("2.2 High-Level System Architecture Design")
    p(
        "PharmaCare implements a decoupled, three-tier architecture adhering to modern microservice and client-server standards. "
        "As illustrated in Figure 1, the presentation layer communicates with the backend via two dedicated transport channels: "
        "standard stateless HTTPS REST endpoints for transactional CRUD operations, and persistent, low-overhead WebSocket (WSS) tunnels "
        "managed via Socket.IO for event-driven push notifications."
    )
    add_figure("report_assets/figure1_architecture.png", "Figure 1: PharmaCare 3-Tier Enterprise System Architecture")

    h2("2.3 Data Flow & FEFO Algorithmic Design")
    p(
        "The core mathematical and business innovation in PharmaCare is its First-Expiry, First-Out (FEFO) dispensing algorithm. "
        "When an item is added to the dispensary checkout cart with requested quantity Q, the backend does not simply deduct units "
        "from an arbitrary aggregate counter. Instead, it queries all unexpired, active inventory batches for that medicine and orders them "
        "in ascending chronological order of expiration dates (expiryDate ASC). As detailed in the flowchart in Figure 2, the algorithm "
        "deducts stock sequentially from the earliest expiring batch. If that batch contains fewer units than requested, it depletes that batch "
        "and cascades to the next batch until the full quantity is fulfilled, recording exact batch allocations on the resulting invoice."
    )
    add_figure("report_assets/figure2_fefo_flowchart.png", "Figure 2: First-Expiry, First-Out (FEFO) Batch Allocation Logic Flowchart")

    h2("2.4 Database Schema & Persistence Architecture")
    p(
        "The persistence layer utilizes MongoDB Atlas structured via Mongoose Object Data Modeling (ODM) schemas. "
        "The primary schemas and relationships include:"
    )
    bullet("User Schema", "Stores user identities, hashed passwords (bcrypt), system roles (admin vs cashier), email indices, and session audit timestamps.")
    bullet("Medication Schema", "Defines the pharmaceutical catalog containing brand name, generic salt composition, manufacturer, therapeutic category, dosage form (Tablet, Syrup, Injection, Capsule), Schedule classification (Schedule-H flag), minimum reorder threshold, and barcode string.")
    bullet("Batch Schema", "Linked to Medication via foreign key (medicineId). Stores batch number, manufacturing date, expiration date, cost price, MRP per unit, initial received quantity, and real-time available stock balance.")
    bullet("Sale & SaleItem Schemas", "Captures transactional invoices containing invoice number, customer name, mobile number, prescribing doctor details, line items (with itemized batch IDs), GST calculations (CGST/SGST), total bill amount, payment mode, and cashier ID.")
    bullet("Purchase Order & Supplier Schemas", "Manages external supplier directory (GSTIN, drug license number) and consignment purchase orders transitioning through status states: Draft -> Ordered -> Consignment Received.")

    h2("2.5 RESTful API Specification and WebSocket Protocol")
    p(
        "The Express.js backend exposes clean, versioned, RESTful endpoints grouped into cohesive resource controllers: "
        "/api/auth for authentication, /api/inventory for medicine and batch management, /api/billing for POS checkouts, "
        "/api/sales for invoice history, /api/expiry for shelf-life monitoring, and /api/reports for financial metrics. "
        "In parallel, the Socket.IO subsystem handles events including stock:alert (dispatched when inventory crosses safety thresholds), "
        "sale:completed (updating live revenue widgets on admin dashboards), and expiry:warning (notifying staff of expiring lots)."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: IMPLEMENTATION WITH SCREENSHOTS
    # =========================================================================
    h1("3. Implementation with Screenshots")

    h2("3.1 Authentication & Role-Based Access Control (RBAC)")
    p(
        "PharmaCare implements rigorous, stateless authentication utilizing JSON Web Tokens (JWT). "
        "Upon successful credential verification via bcrypt comparison (salt rounds: 10), the server issues a signed JWT payload "
        "containing the user's unique ID, username, email, and authorization role (admin or cashier). "
        "Protected backend routes are guarded by high-order middleware functions (requireAuth and requireAdmin). "
        "If a cashier session attempts an administrative action (e.g., manual stock adjustment or deleting a medicine), the backend "
        "immediately intercepts the request and responds with an HTTP 403 Forbidden status."
    )

    h2("3.2 Intelligent FEFO POS Billing Interface")
    p(
        "The Point of Sale billing interface is optimized for high-speed counter operations. "
        "Cashiers can instantly lookup medicines via live text queries or barcode scanner inputs. "
        "As shown in Figure 3, the POS terminal features a split-pane layout: the left pane houses the real-time active cart "
        "displaying medicine names, automatically allocated batch numbers, expiry months, unit prices, and sub-totals. "
        "The right pane computes live tax breakdowns, including Central GST (CGST) and State GST (SGST), discounts, round-off adjustments, "
        "and payment method toggles (Cash, Card, UPI). For Schedule-H drugs, the UI enforces patient name and prescribing doctor recording "
        "prior to checkout completion."
    )
    add_figure("report_assets/figure3_pos_billing.png", "Figure 3: PharmaCare Intelligent Point-of-Sale (POS) Billing Interface")

    h2("3.3 Clinical Inventory and Batch Management")
    p(
        "The inventory catalog view provides pharmacists with comprehensive visibility across all active medicine formulations. "
        "As depicted in Figure 4, the catalog lists brand names, generic formulations, batch numbers, expiration timelines, unit MRPs, "
        "and real-time stock balances. Each medicine displays color-coded status badges: In Stock (green), Low Stock (amber), "
        "Expiring Soon (orange), and Out of Stock (red). Administrators can click any medicine row to view complete historical lot movements, "
        "provision new batches, or execute audited stock quantity corrections."
    )
    add_figure("report_assets/figure4_inventory_catalog.png", "Figure 4: Clinical Medication Catalog and Multi-Batch Tracking Interface")

    h2("3.4 Shelf-Life Monitoring and Expiry Protocol")
    p(
        "To systematically prevent aged medication losses, PharmaCare features a dedicated Expiry Management subsystem. "
        "As illustrated in Figure 5, inventory lots are automatically segmented into chronological hazard intervals: "
        "<7 Days, <30 Days, <90 Days, and Already Expired. Pharmacists can trigger one-click clinical disposal workflows, "
        "which mark batches as written-off, log regulatory destruction reasons, deduct the items from dispensable stock, "
        "and record the financial loss in the audit ledger."
    )
    add_figure("report_assets/figure5_expiry_management.png", "Figure 5: PharmaCare Shelf-Life Monitoring and Expiry Disposal Management Dashboard")

    h2("3.5 Executive Financial Analytics & Visual Reporting")
    p(
        "For store owners and dispensary directors, PharmaCare provides real-time business intelligence dashboards built with Recharts. "
        "As shown in Figure 6, the analytics module displays primary key performance indicators: Gross Revenue, Invoice Volume, "
        "Total Inventory Asset Valuation, and Net Operating Margin. Visual charts breakdown sales revenue by pharmaceutical categories "
        "(Antibiotics, Cardiovascular, Gastrointestinal, Antidiabetics), alongside a dispensary cashier reconciliation leaderboard "
        "ensuring zero cash register variance between work shifts."
    )
    add_figure("report_assets/figure6_analytics_reports.png", "Figure 6: Executive Financial Analytics & Category Sales Performance Dashboard")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: DEPLOYMENT AND DEVOPS
    # =========================================================================
    h1("4. Deployment and DevOps")

    h2("4.1 Multi-Container Docker Architecture")
    p(
        "PharmaCare is fully containerized using Docker to eliminate environment discrepancies ('works on my machine' syndrome) "
        "and ensure rapid, reproducible deployments across developer machines, staging clusters, and production cloud servers. "
        "Both the Next.js frontend client and Express.js backend server utilize optimized multi-stage Dockerfiles: "
        "the build stages compile TypeScript assets and Next.js static bundles, while the lightweight production runtime stages copy "
        "only compiled artifacts and production dependencies, reducing container image sizes by over 65%."
    )

    h2("4.2 Docker Compose Runtime Orchestration")
    p(
        "The multi-service ecosystem is orchestrated via Docker Compose (docker-compose.yml and docker-compose.prod.yml). "
        "The orchestration defines four coordinated services interconnected via an isolated internal bridge network:"
    )
    bullet("pharmacare-server", "Node.js Express REST API & Socket.IO runtime executing on port 5001 with automated healthcheck probes (wget /api/health).")
    bullet("pharmacare-client", "Next.js 14 SSR frontend serving on port 3000, depending on healthy server status.")
    bullet("pharmacare-proxy (Nginx)", "Acts as an edge reverse proxy routing incoming port 80/443 traffic to the client and /api calls to the backend container.")
    bullet("pharmacare-mongo", "Containerized local database service with persistent Docker volume mappings.")

    h2("4.3 Automated CI/CD Pipeline via GitHub Actions")
    p(
        "Continuous Integration and Continuous Deployment (CI/CD) is automated using GitHub Actions (.github/workflows/ci.yml). "
        "As visualized in Figure 7, every git commit pushed to the main branch or Pull Request automatically triggers a 3-stage validation pipeline:"
    )
    bullet("Stage 1 — Backend Lint & Unit/Integration Tests", "Installs dependencies, executes Jest test suites covering FEFO batch allocation logic and auth RBAC middleware, and compiles TypeScript into executable JavaScript.")
    bullet("Stage 2 — Frontend Build & Typecheck", "Validates TypeScript interfaces, compiles Next.js App Router bundles, and ensures zero linting errors.")
    bullet("Stage 3 — Docker Build Verification", "Builds multi-platform Docker container images for both client and server to verify deployment integrity.")
    add_figure("report_assets/figure7_devops_pipeline.png", "Figure 7: PharmaCare DevOps Architecture and GitHub Actions CI/CD Pipeline Workflow")

    h2("4.4 Production Cloud Deployment & Security Hardening")
    p(
        "The live production application is deployed on the Render cloud platform with MongoDB Atlas cloud clusters. "
        "Production security hardening measures implemented include:"
    )
    bullet("Helmet Security Headers", "Enforces Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), X-Frame-Options (DENY), and X-XSS-Protection.")
    bullet("Express Rate Limiting", "Protects authentication routes (/api/auth/login) against automated brute-force attacks by limiting requests to 10 attempts per IP per 15-minute window.")
    bullet("CORS Origin Restriction", "Restricts cross-origin resource sharing strictly to configured frontend domain origins.")
    bullet("Cryptographic Password Salting", "Passwords hashed using bcryptjs with 10 salt rounds, preventing rainbow-table precomputation.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    h1("5. Conclusion and Future Scope")

    h2("5.1 Summary of Accomplishments")
    p(
        "The PharmaCare Mini-Project successfully demonstrates the design, full-stack engineering, and cloud deployment of a robust, "
        "enterprise-grade pharmacy management application. Key project milestones accomplished include:"
    )
    bullet("Elimination of Expiry Losses", "The automated FEFO algorithm successfully dispenses earliest expiring medicine batches, solving the primary cause of dead inventory in retail pharmacies.")
    bullet("Rapid Counter Throughput", "The streamlined POS checkout interface reduces customer transaction time from minutes to seconds with automatic tax computation and receipt generation.")
    bullet("Full Regulatory Compliance", "Batch-level traceability and mandatory Schedule-H prescription recording ensure compliance with Indian drug regulatory mandates.")
    bullet("Production-Ready DevOps Pipeline", "Containerization with Docker, multi-service orchestration with Docker Compose, and automated CI/CD via GitHub Actions establish an enterprise standard of maintainability.")

    h2("5.2 Future Enhancements & Commercial Roadmap")
    p(
        "Building upon the proven foundation established in this project, future development phases will incorporate the following advanced capabilities:"
    )
    bullet("AI-Powered Demand & Reorder Forecasting", "Integrate machine learning predictive models (ARIMA / LSTM) to analyze seasonal disease trends and automatically recommend purchase order quantities for critical drugs.")
    bullet("Automated WhatsApp & SMS Invoice Dispatch", "Integrate the WhatsApp Business Cloud API to deliver digital, paperless GST tax invoices and dosage reminders directly to patients' smartphones.")
    bullet("Drug-Drug Interaction & Allergy Checker", "Integrate medical reference APIs to provide instant clinical contraindication warnings at the POS terminal when a doctor prescribes potentially conflicting drug combinations.")
    bullet("Mobile Dispensary Companion App", "Develop a cross-platform mobile application using React Native allowing dispensary managers to audit inventory and scan barcodes directly from handheld smartphones.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: GITHUB REPOSITORY & LIVE DEPLOYMENT
    # =========================================================================
    h1("6. GitHub Repository and Live Deployment Links")

    p(
        "All source code, configuration files, Docker container recipes, automated test suites, and documentation for the "
        "PharmaCare project have been committed, version-controlled, and published on GitHub, alongside a live production deployment on Render."
    )

    # Repository & Link Information Table
    repo_table = doc.add_table(rows=5, cols=2)
    repo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    repo_data = [
        ("Official GitHub Repository:", "https://github.com/kirteexh/FSD_MiniProject"),
        ("Live Cloud Production Deployment:", "https://fsd-miniproject-skab.onrender.com"),
        ("Backend Health Check Endpoint:", "https://fsd-miniproject-skab.onrender.com/api/health"),
        ("Primary Author & Developer:", "Kirteesh Dattatray Rakshe (Roll No. 43, Class D15A)"),
        ("License & Rights:", "MIT Open Source License (2026)")
    ]
    for i, (k, v) in enumerate(repo_data):
        row = repo_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.4)
        c1.width = Inches(3.8)
        set_cell_background(c0, "0F172A" if i==0 else "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=70, bottom=70, left=90, right=90)
        set_cell_margins(c1, top=70, bottom=70, left=90, right=90)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.1
        r0 = p0.add_run(k)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        if i == 0:
            r0.font.color.rgb = RGBColor(255, 255, 255)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.1
        r1 = p1.add_run(v)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        if "http" in v:
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(2, 132, 199)

    p(space_after=14)
    p(
        "To clone, run, and evaluate the complete project locally, execute the following standard sequence in terminal:"
    )

    p("git clone https://github.com/kirteexh/FSD_MiniProject.git\ncd FSD_MiniProject\nnpm run install:all\nnpm run dev", 
      bold=True, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, color=RGBColor(30, 41, 59))

    p(space_after=20)
    p("— End of Mini-Project Report —", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Save to Word Document
    out_filename = "FSD_Mini_Project_Report_Kirteesh_Rakshe.docx"
    doc.save(out_filename)
    print(f"Report generated successfully: {out_filename}")

    # Also copy to Pharmacy Management System folder so it is in both places
    dest_copy = os.path.join(r"C:\Users\kirte\OneDrive\Desktop\3rd Year\FSD\Pharmacy Management System", out_filename)
    try:
        doc.save(dest_copy)
        print(f"Copied report to: {dest_copy}")
    except Exception as e:
        print(f"Could not copy to {dest_copy}: {e}")

if __name__ == "__main__":
    generate_report()
