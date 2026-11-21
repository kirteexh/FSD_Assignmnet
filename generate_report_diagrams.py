import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('report_assets', exist_ok=True)

def get_font(size, bold=False):
    # Try common Windows fonts
    font_names = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf"
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except:
                pass
    return ImageFont.load_default()

# -----------------------------------------------------------------------------
# 1. System Architecture Diagram
# -----------------------------------------------------------------------------
def make_architecture_diagram():
    img = Image.new('RGB', (1200, 680), '#0b1120')
    d = ImageDraw.Draw(img)
    
    font_title = get_font(24, bold=True)
    font_sub = get_font(14)
    font_box_title = get_font(16, bold=True)
    font_item = get_font(13)
    font_badge = get_font(11, bold=True)
    
    # Title
    d.text((40, 30), "PharmaCare System Architecture & Component Interaction", fill='#f8fafc', font=font_title)
    d.text((40, 65), "3-Tier Decoupled Architecture with Next.js 14, Express REST/Socket.IO & MongoDB Atlas", fill='#94a3b8', font=font_sub)
    
    # Tier 1: Client Tier
    d.rounded_rectangle([40, 110, 380, 620], radius=12, fill='#1e293b', outline='#3b82f6', width=2)
    d.text((60, 130), "CLIENT PRESENTATION TIER", fill='#60a5fa', font=font_badge)
    d.text((60, 150), "Next.js 14 Web Application", fill='#ffffff', font=font_box_title)
    
    client_items = [
        ("App Router & SSR / Client Components", "app/dashboard, app/billing, app/inventory"),
        ("State Management: Redux Toolkit", "Cart, Auth, Notifications, Real-time feeds"),
        ("UI System: Tailwind CSS & Framer Motion", "Clinical theme, responsive grid, animations"),
        ("Data Visualization: Recharts", "Executive sales charts, expiry breakdowns"),
        ("Client Interceptor: Typed REST Client", "Automatic Bearer token injection, 401 handling"),
        ("Real-Time Client: Socket.IO Client", "WebSocket connection for live low-stock alerts")
    ]
    y = 200
    for title, desc in client_items:
        d.rounded_rectangle([60, y, 360, y + 54], radius=6, fill='#0f172a', outline='#334155', width=1)
        d.text((72, y + 8), title, fill='#f1f5f9', font=font_item)
        d.text((72, y + 28), desc, fill='#64748b', font=get_font(11))
        y += 66

    # Tier 2: Server / Application Tier
    d.rounded_rectangle([420, 110, 780, 620], radius=12, fill='#1e293b', outline='#10b981', width=2)
    d.text((440, 130), "APPLICATION SERVICES TIER", fill='#34d399', font=font_badge)
    d.text((440, 150), "Node.js & Express REST API", fill='#ffffff', font=font_box_title)
    
    server_items = [
        ("Security Middleware Stack", "Helmet (headers), CORS, Express Rate Limit"),
        ("Authentication & RBAC Engine", "JWT signing & verification, bcryptjs (salt: 10)"),
        ("FEFO Billing Business Service", "Atomic batch allocation, concurrency mutex"),
        ("Inventory & Stock Movement Engine", "Batch lifecycle, shelf-life triggers, disposal audit"),
        ("Real-Time Notification Hub", "Socket.IO server broadcasting stock events"),
        ("Purchase Order Lifecycle Manager", "Procurement, consignment receipt & auto-intake")
    ]
    y = 200
    for title, desc in server_items:
        d.rounded_rectangle([440, y, 760, y + 54], radius=6, fill='#0f172a', outline='#334155', width=1)
        d.text((452, y + 8), title, fill='#f1f5f9', font=font_item)
        d.text((452, y + 28), desc, fill='#64748b', font=get_font(11))
        y += 66

    # Tier 3: Persistence & Cloud Tier
    d.rounded_rectangle([820, 110, 1160, 620], radius=12, fill='#1e293b', outline='#8b5cf6', width=2)
    d.text((840, 130), "DATA PERSISTENCE & DEVOPS", fill='#a78bfa', font=font_badge)
    d.text((840, 150), "Storage & Infrastructure", fill='#ffffff', font=font_box_title)
    
    storage_items = [
        ("MongoDB Atlas (Cloud Cluster)", "Mongoose ODM models, indexed collections"),
        ("Dual-Mode Fallback Store", "In-memory seeded store for rapid evaluation"),
        ("Nginx Reverse Proxy", "SSL termination, port 80/443 routing, gzip"),
        ("Docker Containerization", "Multi-stage Dockerfiles for client & server"),
        ("Docker Compose Orchestrator", "Multi-service container runtime network"),
        ("CI/CD Pipeline (GitHub Actions)", "Automated lint, test, build, image packaging")
    ]
    y = 200
    for title, desc in storage_items:
        d.rounded_rectangle([840, y, 1140, y + 54], radius=6, fill='#0f172a', outline='#334155', width=1)
        d.text((852, y + 8), title, fill='#f1f5f9', font=font_item)
        d.text((852, y + 28), desc, fill='#64748b', font=get_font(11))
        y += 66

    # Connection Arrows
    d.line([(380, 240), (420, 240)], fill='#38bdf8', width=3)
    d.polygon([(420, 240), (412, 235), (412, 245)], fill='#38bdf8')
    d.text((385, 220), "REST", fill='#38bdf8', font=get_font(10, bold=True))
    
    d.line([(380, 480), (420, 480)], fill='#f59e0b', width=3)
    d.polygon([(420, 480), (412, 475), (412, 485)], fill='#f59e0b')
    d.text((385, 460), "WS", fill='#f59e0b', font=get_font(10, bold=True))

    d.line([(780, 240), (820, 240)], fill='#34d399', width=3)
    d.polygon([(820, 240), (812, 235), (812, 245)], fill='#34d399')
    d.text((785, 220), "TCP", fill='#34d399', font=get_font(10, bold=True))

    img.save("report_assets/figure1_architecture.png")
    print("Saved figure1_architecture.png")

# -----------------------------------------------------------------------------
# 2. FEFO Algorithm Flowchart
# -----------------------------------------------------------------------------
def make_fefo_flowchart():
    img = Image.new('RGB', (1200, 640), '#ffffff')
    d = ImageDraw.Draw(img)
    
    font_title = get_font(22, bold=True)
    font_sub = get_font(13)
    font_node = get_font(12, bold=True)
    font_label = get_font(11)
    
    # Title
    d.text((40, 25), "First-Expiry, First-Out (FEFO) Inventory Allocation Logic", fill='#0f172a', font=font_title)
    d.text((40, 55), "Algorithmic decision tree ensuring aged pharmaceutical stock is dispensed before fresher inventory", fill='#475569', font=font_sub)
    
    # Flowchart boxes
    # Step 1: Start
    d.rounded_rectangle([60, 110, 220, 170], radius=10, fill='#0284c7', outline='#0369a1', width=2)
    d.text((80, 130), "POS Item Scanned", fill='#ffffff', font=font_node)
    d.text((80, 146), "Qty Requested = Q", fill='#e0f2fe', font=font_label)

    # Arrow 1->2
    d.line([(220, 140), (280, 140)], fill='#64748b', width=2)
    d.polygon([(280, 140), (272, 135), (272, 145)], fill='#64748b')

    # Step 2: Query active batches
    d.rounded_rectangle([280, 110, 470, 170], radius=8, fill='#f1f5f9', outline='#cbd5e1', width=2)
    d.text((295, 125), "Fetch Active Batches", fill='#0f172a', font=font_node)
    d.text((295, 142), "Filter: unexpired, qty > 0", fill='#475569', font=font_label)
    d.text((295, 155), "Sort: expiryDate ASC", fill='#0284c7', font=font_label)

    # Arrow 2->3
    d.line([(470, 140), (530, 140)], fill='#64748b', width=2)
    d.polygon([(530, 140), (522, 135), (522, 145)], fill='#64748b')

    # Step 3: Decision: Total Stock >= Q?
    d.polygon([(620, 100), (710, 140), (620, 180), (530, 140)], fill='#fef3c7', outline='#d97706', width=2)
    d.text((570, 132), "Stock >= Q?", fill='#92400e', font=font_node)

    # Arrow 3->No (Insufficient)
    d.line([(620, 180), (620, 250)], fill='#dc2626', width=2)
    d.polygon([(620, 250), (615, 242), (625, 242)], fill='#dc2626')
    d.text((626, 205), "NO", fill='#dc2626', font=get_font(11, bold=True))

    d.rounded_rectangle([530, 250, 710, 310], radius=8, fill='#fee2e2', outline='#ef4444', width=2)
    d.text((545, 268), "Reject Transaction", fill='#b91c1c', font=font_node)
    d.text((545, 285), "Error: Insufficient Stock", fill='#7f1d1d', font=font_label)

    # Arrow 3->Yes
    d.line([(710, 140), (770, 140)], fill='#16a34a', width=2)
    d.polygon([(770, 140), (762, 135), (762, 145)], fill='#16a34a')
    d.text((722, 122), "YES", fill='#16a34a', font=get_font(11, bold=True))

    # Step 4: Loop through batches
    d.rounded_rectangle([770, 105, 960, 175], radius=8, fill='#f1f5f9', outline='#cbd5e1', width=2)
    d.text((785, 120), "Select Earliest Batch (B)", fill='#0f172a', font=font_node)
    d.text((785, 137), "Take = min(Q, B.stock)", fill='#475569', font=font_label)
    d.text((785, 153), "B.stock = B.stock - Take", fill='#0284c7', font=font_label)

    # Arrow 4->5
    d.line([(960, 140), (1010, 140), (1010, 240), (960, 240)], fill='#64748b', width=2)
    d.polygon([(960, 240), (968, 235), (968, 245)], fill='#64748b')

    # Step 5: Remaining Q = Q - Take
    d.rounded_rectangle([770, 210, 960, 270], radius=8, fill='#f8fafc', outline='#94a3b8', width=2)
    d.text((785, 225), "Update Remaining Q", fill='#0f172a', font=font_node)
    d.text((785, 245), "Q_rem = Q - Take", fill='#475569', font=font_label)

    # Decision: Q_rem > 0?
    d.polygon([(865, 300), (935, 340), (865, 380), (795, 340)], fill='#fef3c7', outline='#d97706', width=2)
    d.text((825, 332), "Q_rem > 0?", fill='#92400e', font=font_node)

    d.line([(865, 270), (865, 300)], fill='#64748b', width=2)

    # Loop back if YES
    d.line([(935, 340), (980, 340), (980, 140), (960, 140)], fill='#d97706', width=2)
    d.text((940, 322), "YES (Next Batch)", fill='#d97706', font=get_font(10, bold=True))

    # Complete if NO
    d.line([(865, 380), (865, 430)], fill='#16a34a', width=2)
    d.polygon([(865, 430), (860, 422), (870, 422)], fill='#16a34a')
    d.text((875, 400), "NO (Fulfilled)", fill='#16a34a', font=get_font(10, bold=True))

    # Step 6: Atomic Commit
    d.rounded_rectangle([750, 430, 980, 520], radius=10, fill='#dcfce7', outline='#16a34a', width=2)
    d.text((770, 450), "Commit Transaction & Save", fill='#14532d', font=font_node)
    d.text((770, 470), "1. Record Sale & Generate Invoice", fill='#166534', font=font_label)
    d.text((770, 488), "2. Persist Batches & Audit Trail", fill='#166534', font=font_label)
    d.text((770, 504), "3. Emit WebSocket Low-Stock Alert", fill='#166534', font=font_label)

    img.save("report_assets/figure2_fefo_flowchart.png")
    print("Saved figure2_fefo_flowchart.png")

# -----------------------------------------------------------------------------
# 3. POS Billing UI Graphic Mockup
# -----------------------------------------------------------------------------
def make_pos_billing_ui():
    img = Image.new('RGB', (1200, 720), '#090d16')
    d = ImageDraw.Draw(img)
    
    font_bold = get_font(14, bold=True)
    font_regular = get_font(12)
    font_title = get_font(18, bold=True)
    font_code = get_font(11)
    
    # Header bar
    d.rectangle([0, 0, 1200, 50], fill='#0f172a', outline='#1e293b', width=1)
    d.text((24, 15), "PharmaCare POS Billing Engine", fill='#38bdf8', font=font_bold)
    d.text((360, 16), "Active Register #01 | Dispenser: Cashier Staff", fill='#94a3b8', font=font_regular)
    d.text((1050, 16), "Status: ONLINE", fill='#34d399', font=font_bold)
    
    # Left Pane: Product Search & Cart
    d.rounded_rectangle([20, 70, 780, 690], radius=8, fill='#111827', outline='#1f293d', width=1)
    d.text((40, 88), "POINT OF SALE // DISPENSARY CART", fill='#f8fafc', font=font_bold)
    
    # Barcode input bar
    d.rounded_rectangle([40, 120, 760, 160], radius=6, fill='#090d16', outline='#3b82f6', width=1)
    d.text((54, 132), "Scan Barcode or Search Medicine: 8901088001016 (Amoxicillin 500mg)", fill='#93c5fd', font=font_regular)
    
    # Cart Table
    headers = ["Item Name", "Batch #", "Expiry", "Price", "Qty", "Subtotal", "Actions"]
    xs = [40, 240, 360, 460, 540, 620, 710]
    d.rectangle([40, 180, 760, 210], fill='#1e293b')
    for h, x in zip(headers, xs):
        d.text((x + 8, 188), h, fill='#cbd5e1', font=font_bold)
        
    items = [
        ("Amoxicillin 500mg (Cap)", "AMX-2024-B1", "04/2027", "₹ 85.00", "2", "₹ 170.00"),
        ("Paracetamol 650mg Dolo", "DOL-2025-A2", "11/2026", "₹ 30.00", "1", "₹ 30.00"),
        ("Azithromycin 500mg Tab", "AZI-2024-C9", "08/2026", "₹ 120.00", "1", "₹ 120.00"),
        ("Cetirizine 10mg Strip", "CET-2025-D1", "01/2028", "₹ 25.00", "2", "₹ 50.00"),
        ("Pantoprazole 40mg Tab", "PAN-2024-E4", "09/2026", "₹ 95.00", "1", "₹ 95.00")
    ]
    y = 215
    for item in items:
        d.rectangle([40, y, 760, y + 42], fill='#0f172a' if (y//42)%2==0 else '#111827', outline='#1f293d')
        for val, x in zip(item, xs[:-1]):
            d.text((x + 8, y + 12), val, fill='#f1f5f9', font=font_regular)
        d.text((xs[-1] + 8, y + 12), "[ Remove ]", fill='#f43f5e', font=font_code)
        y += 44
        
    # Schedule-H Notification Box
    d.rounded_rectangle([40, y + 20, 760, y + 80], radius=6, fill='#292211', outline='#f59e0b', width=1)
    d.text((54, y + 32), "⚠️ SCHEDULE-H WARNING: Prescription Validation Required", fill='#fbbf24', font=font_bold)
    d.text((54, y + 52), "Prescribing Doctor: Dr. S. R. Joshi, MBBS, MD | Registration #MC-448921 | Patient: Rahul Verma", fill='#fef3c7', font=font_regular)

    # Right Pane: Checkout & Invoice Summary
    d.rounded_rectangle([810, 70, 1180, 690], radius=8, fill='#111827', outline='#1f293d', width=1)
    d.text((830, 88), "ORDER SUMMARY // PAYMENT", fill='#f8fafc', font=font_bold)
    
    summary_fields = [
        ("Gross Total:", "₹ 465.00"),
        ("Trade Discount (5%):", "- ₹ 23.25"),
        ("Taxable Amount:", "₹ 441.75"),
        ("Central GST (CGST 6%):", "₹ 26.50"),
        ("State GST (SGST 6%):", "₹ 26.50"),
        ("Round Off Adjustment:", "+ ₹ 0.25"),
        ("Net Payable Amount:", "₹ 495.00")
    ]
    sy = 130
    for label, val in summary_fields:
        d.text((830, sy), label, fill='#94a3b8' if "Net" not in label else '#38bdf8', font=font_bold if "Net" in label else font_regular)
        d.text((1070, sy), val, fill='#ffffff' if "Net" not in label else '#34d399', font=font_title if "Net" in label else font_bold)
        d.line([(830, sy + 25), (1160, sy + 25)], fill='#1f293d', width=1)
        sy += 36
        
    d.text((830, sy + 15), "Select Payment Mode:", fill='#cbd5e1', font=font_bold)
    d.rounded_rectangle([830, sy + 40, 930, sy + 80], radius=6, fill='#1e293b', outline='#3b82f6', width=2)
    d.text((860, sy + 52), "CASH", fill='#60a5fa', font=font_bold)
    
    d.rounded_rectangle([945, sy + 40, 1045, sy + 80], radius=6, fill='#0f172a', outline='#334155', width=1)
    d.text((975, sy + 52), "UPI", fill='#94a3b8', font=font_bold)
    
    d.rounded_rectangle([1060, sy + 40, 1160, sy + 80], radius=6, fill='#0f172a', outline='#334155', width=1)
    d.text((1085, sy + 52), "CARD", fill='#94a3b8', font=font_bold)
    
    d.rounded_rectangle([830, 600, 1160, 660], radius=8, fill='#10b981', outline='#059669', width=1)
    d.text((920, 622), "COMPLETE SALE & PRINT BILL", fill='#ffffff', font=font_bold)

    img.save("report_assets/figure3_pos_billing.png")
    print("Saved figure3_pos_billing.png")

# -----------------------------------------------------------------------------
# 4. Inventory Catalog & Multi-Batch Tracking UI
# -----------------------------------------------------------------------------
def make_inventory_ui():
    img = Image.new('RGB', (1200, 680), '#090d16')
    d = ImageDraw.Draw(img)
    
    font_bold = get_font(14, bold=True)
    font_regular = get_font(12)
    font_badge = get_font(11, bold=True)
    
    # Top Bar
    d.rectangle([0, 0, 1200, 50], fill='#0f172a', outline='#1e293b')
    d.text((24, 15), "PharmaCare Clinical Inventory & Batch Catalog", fill='#38bdf8', font=font_bold)
    d.text((850, 15), "Total Medicines: 142 | Active Batches: 384", fill='#94a3b8', font=font_regular)
    
    # Filter Row
    d.rounded_rectangle([24, 70, 1176, 120], radius=6, fill='#111827', outline='#1f293d')
    d.text((40, 85), "Search Catalog: [ Type Medicine Name, Generic Salt, or Batch... ]", fill='#64748b', font=font_regular)
    d.text((800, 85), "Filters: [ All Categories ▾ ]  [ Stock Status ▾ ]  [ Schedule ▾ ]", fill='#93c5fd', font=font_regular)
    
    # Inventory Table
    headers = ["Medicine Name", "Category", "Batch Number", "Expiry Date", "Unit MRP", "Available Qty", "Status"]
    xs = [40, 280, 430, 580, 720, 860, 1010]
    d.rectangle([24, 140, 1176, 175], fill='#1e293b')
    for h, x in zip(headers, xs):
        d.text((x, 150), h, fill='#e2e8f0', font=font_bold)
        
    meds = [
        ("Augmentin 625mg Duo", "Antibiotic", "AUG-24-001", "14/05/2026", "₹ 204.00", "140 Tabs", "IN STOCK", '#10b981'),
        ("Telmisartan 40mg Tab", "Cardiovascular", "TEL-25-112", "22/11/2027", "₹ 78.50", "480 Tabs", "IN STOCK", '#10b981'),
        ("Metformin 500mg SR", "Antidiabetic", "MET-24-889", "05/01/2027", "₹ 42.00", "310 Tabs", "IN STOCK", '#10b981'),
        ("Atorvastatin 10mg Tab", "Lipid Lowering", "ATO-23-401", "12/03/2026", "₹ 110.00", "18 Tabs", "LOW STOCK", '#f59e0b'),
        ("Ciprofloxacin Eye Drop", "Ophthalmic", "CIP-24-009", "18/12/2025", "₹ 55.00", "0 Units", "OUT OF STOCK", '#ef4444'),
        ("Rabeprazole 20mg Tab", "Gastrointestinal", "RAB-24-302", "10/08/2026", "₹ 82.00", "220 Tabs", "IN STOCK", '#10b981'),
        ("Montelukast + Levocet", "Respiratory", "MON-24-510", "28/04/2026", "₹ 135.00", "85 Tabs", "IN STOCK", '#10b981'),
        ("Insulin Glargine Pen", "Endocrine", "INS-24-002", "15/02/2026", "₹ 650.00", "4 Pens", "EXPIRING SOON", '#f97316')
    ]
    y = 180
    for med in meds:
        d.rectangle([24, y, 1176, y + 54], fill='#0f172a' if (y//54)%2==0 else '#111827', outline='#1f293d')
        for val, x in zip(med[:-2], xs[:-2]):
            d.text((x, y + 16), val, fill='#f1f5f9', font=font_regular)
        d.text((xs[-2], y + 16), med[-2], fill='#38bdf8', font=font_bold)
        
        # Status Badge
        badge_color = med[-1]
        d.rounded_rectangle([xs[-1], y + 12, xs[-1] + 120, y + 38], radius=4, fill='#161f2e', outline=badge_color, width=1)
        d.text((xs[-1] + 14, y + 18), med[-2+1], fill=badge_color, font=font_badge)
        y += 56

    img.save("report_assets/figure4_inventory_catalog.png")
    print("Saved figure4_inventory_catalog.png")

# -----------------------------------------------------------------------------
# 5. Expiry Management UI
# -----------------------------------------------------------------------------
def make_expiry_ui():
    img = Image.new('RGB', (1200, 640), '#090d16')
    d = ImageDraw.Draw(img)
    
    font_bold = get_font(14, bold=True)
    font_regular = get_font(12)
    font_title = get_font(18, bold=True)
    font_kpi = get_font(24, bold=True)
    
    # Header
    d.rectangle([0, 0, 1200, 50], fill='#0f172a', outline='#1e293b')
    d.text((24, 15), "PharmaCare Shelf-Life & Expiry Management Protocol", fill='#38bdf8', font=font_bold)
    
    # 4 KPI Cards for Expiry Windows
    kpis = [
        ("Expiring in < 7 Days", "3 Batches", "₹ 4,820 Risk", '#ef4444'),
        ("Expiring in < 30 Days", "8 Batches", "₹ 14,250 Value", '#f97316'),
        ("Expiring in < 90 Days", "19 Batches", "₹ 38,100 Value", '#f59e0b'),
        ("Written-Off (Expired)", "2 Batches", "Disposed / Logged", '#64748b')
    ]
    kx = 24
    for title, count, val, color in kpis:
        d.rounded_rectangle([kx, 70, kx + 270, 170], radius=8, fill='#111827', outline=color, width=2)
        d.text((kx + 16, 85), title, fill='#94a3b8', font=font_bold)
        d.text((kx + 16, 110), count, fill=color, font=font_kpi)
        d.text((kx + 16, 144), val, fill='#cbd5e1', font=font_regular)
        kx += 295
        
    # Table of Urgent Action Items
    d.text((24, 200), "URGENT CLINICAL DISPOSAL & RETURN QUEUE", fill='#f8fafc', font=font_bold)
    headers = ["Medicine Name", "Batch #", "Manufacturer", "Expiry Date", "Current Stock", "Action Workflow"]
    xs = [40, 280, 440, 640, 800, 980]
    d.rectangle([24, 230, 1176, 265], fill='#1e293b')
    for h, x in zip(headers, xs):
        d.text((x, 240), h, fill='#e2e8f0', font=font_bold)
        
    rows = [
        ("Ceftriaxone 1g Vial Inj", "CFX-23-901", "Alkem Labs", "28/11/2026 (7d)", "12 Vials", "[ Record Clinical Disposal ]"),
        ("Paracetamol 120mg Syr", "PCM-24-110", "Cipla Ltd", "02/12/2026 (11d)", "24 Bottles", "[ Vendor Return Request ]"),
        ("Erythromycin 250mg Tab", "ERY-23-455", "Sun Pharma", "14/12/2026 (23d)", "40 Strips", "[ Discount Clearance Sale ]"),
        ("Ofloxacin Eye Ointment", "OFL-24-001", "FDC Pharma", "05/01/2027 (45d)", "18 Tubes", "[ Flagged for Monitoring ]")
    ]
    y = 270
    for r in rows:
        d.rectangle([24, y, 1176, y + 54], fill='#0f172a' if (y//54)%2==0 else '#111827', outline='#1f293d')
        for val, x in zip(r[:-1], xs[:-1]):
            d.text((x, y + 16), val, fill='#f1f5f9', font=font_regular)
        d.text((xs[-1], y + 16), r[-1], fill='#38bdf8' if "Discount" in r[-1] else ('#f43f5e' if "Disposal" in r[-1] else '#f59e0b'), font=font_bold)
        y += 56

    img.save("report_assets/figure5_expiry_management.png")
    print("Saved figure5_expiry_management.png")

# -----------------------------------------------------------------------------
# 6. Financial Reports & Analytics UI
# -----------------------------------------------------------------------------
def make_analytics_ui():
    img = Image.new('RGB', (1200, 640), '#090d16')
    d = ImageDraw.Draw(img)
    
    font_bold = get_font(14, bold=True)
    font_regular = get_font(12)
    font_kpi = get_font(22, bold=True)
    
    # Top Bar
    d.rectangle([0, 0, 1200, 50], fill='#0f172a', outline='#1e293b')
    d.text((24, 15), "PharmaCare Executive Financial & Auditing Analytics", fill='#38bdf8', font=font_bold)
    d.text((880, 15), "Reporting Period: Last 30 Days (November 2026)", fill='#94a3b8', font=font_regular)
    
    # 4 Metric Cards
    metrics = [
        ("Gross Revenue", "₹ 4,82,450.00", "+14.2% vs last month", '#10b981'),
        ("Total Sales Invoices", "1,248 Bills", "Avg ₹ 386.50 / Bill", '#38bdf8'),
        ("Total Inventory Valuation", "₹ 18,92,100.00", "Across 384 active batches", '#818cf8'),
        ("Net Operating Profit", "₹ 1,18,600.00", "24.5% Profit Margin", '#f59e0b')
    ]
    mx = 24
    for title, val, sub, col in metrics:
        d.rounded_rectangle([mx, 70, mx + 270, 165], radius=8, fill='#111827', outline='#1f293d', width=1)
        d.text((mx + 16, 85), title, fill='#94a3b8', font=font_bold)
        d.text((mx + 16, 108), val, fill='#ffffff', font=font_kpi)
        d.text((mx + 16, 140), sub, fill=col, font=font_regular)
        mx += 295
        
    # Simulated Chart Area: Revenue by Category
    d.rounded_rectangle([24, 190, 680, 600], radius=8, fill='#111827', outline='#1f293d')
    d.text((44, 210), "SALES REVENUE BY PHARMACEUTICAL CATEGORY", fill='#f8fafc', font=font_bold)
    
    categories = [
        ("Antibiotics & Antivirals", 380, "₹ 1,42,800 (29.6%)", '#38bdf8'),
        ("Cardiovascular & Hypertension", 310, "₹ 1,12,400 (23.3%)", '#10b981'),
        ("Gastrointestinal & Antacids", 220, "₹ 82,100 (17.0%)", '#818cf8'),
        ("Antidiabetics & Endocrine", 180, "₹ 68,900 (14.3%)", '#f59e0b'),
        ("Analgesics & Antipyretics", 140, "₹ 52,250 (10.8%)", '#f43f5e'),
        ("Vitamins & Supplements", 70, "₹ 24,000 (5.0%)", '#a855f7')
    ]
    cy = 250
    for name, bar_w, val, col in categories:
        d.text((44, cy), name, fill='#cbd5e1', font=font_regular)
        d.rounded_rectangle([44, cy + 20, 44 + bar_w, cy + 38], radius=4, fill=col)
        d.text((44 + bar_w + 14, cy + 22), val, fill='#94a3b8', font=font_regular)
        cy += 54

    # Right Area: Cashier Leaderboard & Audit Status
    d.rounded_rectangle([715, 190, 1176, 600], radius=8, fill='#111827', outline='#1f293d')
    d.text((735, 210), "DISPENSARY CASHIER RECONCILIATION", fill='#f8fafc', font=font_bold)
    
    cashiers = [
        ("Staff Cashier 01 (Morning Shift)", "612 Bills", "₹ 2,44,200.00", "Balanced (0 variance)"),
        ("Staff Cashier 02 (Evening Shift)", "548 Bills", "₹ 1,98,400.00", "Balanced (0 variance)"),
        ("Store Manager Admin (Special)", "88 Bills", "₹ 39,850.00", "Balanced (0 variance)")
    ]
    dy = 260
    for cname, bills, rev, stat in cashiers:
        d.rounded_rectangle([735, dy, 1156, dy + 70], radius=6, fill='#0f172a', outline='#334155')
        d.text((750, dy + 12), cname, fill='#ffffff', font=font_bold)
        d.text((750, dy + 36), f"{bills} processed  |  Total: {rev}", fill='#38bdf8', font=font_regular)
        d.text((1000, dy + 36), stat, fill='#34d399', font=get_font(11, bold=True))
        dy += 84

    img.save("report_assets/figure6_analytics_reports.png")
    print("Saved figure6_analytics_reports.png")

# -----------------------------------------------------------------------------
# 7. DevOps & CI/CD Pipeline Architecture
# -----------------------------------------------------------------------------
def make_devops_diagram():
    img = Image.new('RGB', (1200, 600), '#0b1120')
    d = ImageDraw.Draw(img)
    
    font_title = get_font(22, bold=True)
    font_sub = get_font(13)
    font_node = get_font(13, bold=True)
    font_label = get_font(11)
    
    # Title
    d.text((40, 25), "PharmaCare DevOps Architecture & GitHub Actions CI/CD Pipeline", fill='#f8fafc', font=font_title)
    d.text((40, 55), "Automated multi-stage continuous integration, Docker image packaging, and containerized deployment", fill='#94a3b8', font=font_sub)
    
    # 4 Pipeline Stages
    stages = [
        ("1. Git Commit & Push", "Trigger: push on main branch\n• Developer pushes code\n• GitHub webhook dispatches CI\n• Monorepo change detection", '#3b82f6'),
        ("2. Automated CI Testing", "Job: backend-test-and-build\n• Node.js 18 setup & npm ci\n• Jest unit & integration tests\n• FEFO algorithm verification\n• JWT auth & RBAC route tests", '#10b981'),
        ("3. Client & Server Build", "Job: frontend-build & tsc\n• Next.js 14 SSR/SSG compilation\n• Strict TypeScript type checking\n• Production asset optimization\n• Environment injection", '#8b5cf6'),
        ("4. Docker Containerization", "Job: docker-containers-check\n• Dockerfile multi-stage builds\n• Client & server images built\n• Render & Compose deployment\n• Automated healthcheck probes", '#f59e0b')
    ]
    sx = 40
    for i, (title, desc, col) in enumerate(stages):
        d.rounded_rectangle([sx, 120, sx + 250, 480], radius=10, fill='#1e293b', outline=col, width=2)
        d.rounded_rectangle([sx, 120, sx + 250, 170], radius=10, fill=col)
        d.text((sx + 14, 136), title, fill='#ffffff', font=font_node)
        
        lines = desc.split('\n')
        ly = 195
        for line in lines:
            d.text((sx + 16, ly), line, fill='#e2e8f0', font=font_label)
            ly += 26
            
        if i < 3:
            # Arrow to next stage
            d.line([(sx + 250, 300), (sx + 280, 300)], fill='#38bdf8', width=3)
            d.polygon([(sx + 280, 300), (sx + 272, 294), (sx + 272, 306)], fill='#38bdf8')
            
        sx += 290
        
    # Docker Compose banner at bottom
    d.rounded_rectangle([40, 510, 1160, 570], radius=8, fill='#0f172a', outline='#334155', width=1)
    d.text((60, 525), "Production Runtime Orchestration: docker-compose.prod.yml (Nginx Port 80/443 -> Client Next.js Port 3000 -> Express Server Port 5001 -> MongoDB Atlas)", fill='#38bdf8', font=get_font(12, bold=True))
    d.text((60, 545), "Live Production URL: https://fsd-miniproject-skab.onrender.com | Repository: https://github.com/kirteexh/FSD_MiniProject", fill='#94a3b8', font=font_label)

    img.save("report_assets/figure7_devops_pipeline.png")
    print("Saved figure7_devops_pipeline.png")

if __name__ == "__main__":
    make_architecture_diagram()
    make_fefo_flowchart()
    make_pos_billing_ui()
    make_inventory_ui()
    make_expiry_ui()
    make_analytics_ui()
    make_devops_diagram()
    print("All 7 technical figures successfully generated!")
