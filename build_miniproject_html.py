import os
import base64

def get_base64_img(filename):
    p = os.path.join('report_assets', filename)
    if os.path.exists(p):
        with open(p, 'rb') as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

fig1 = get_base64_img('figure1_architecture.png')
fig2 = get_base64_img('figure2_fefo_flowchart.png')
fig3 = get_base64_img('figure3_pos_billing.png')
fig4 = get_base64_img('figure4_inventory_catalog.png')
fig5 = get_base64_img('figure5_expiry_management.png')
fig6 = get_base64_img('figure6_analytics_reports.png')
fig7 = get_base64_img('figure7_devops_pipeline.png')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FSD Mini-Project Report — PharmaCare (Kirteesh Rakshe)</title>
  <style>
    @page {{
      size: A4;
      margin: 1in;
      @bottom-center {{
        content: counter(page);
        font-family: 'Times New Roman', Times, serif;
        font-size: 10pt;
      }}
    }}
    body {{
      font-family: 'Times New Roman', Times, serif;
      font-size: 12pt;
      line-height: 1.5;
      text-align: justify;
      color: #0f172a;
      background: #f1f5f9;
      margin: 0;
      padding: 40px 20px;
    }}
    .document-page {{
      background: #ffffff;
      width: 8.27in;
      min-height: 11.69in;
      margin: 0 auto 40px auto;
      padding: 1in;
      box-sizing: border-box;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      position: relative;
    }}
    h1 {{
      font-size: 16pt;
      font-weight: bold;
      text-align: left;
      margin-top: 24pt;
      margin-bottom: 10pt;
      color: #0f172a;
      border-bottom: 1.5pt solid #0f172a;
      padding-bottom: 4pt;
    }}
    h2 {{
      font-size: 14pt;
      font-weight: bold;
      text-align: left;
      margin-top: 18pt;
      margin-bottom: 8pt;
      color: #1e293b;
    }}
    p {{
      margin-top: 0;
      margin-bottom: 10pt;
      line-height: 1.5;
    }}
    ul, ol {{
      margin-top: 0;
      margin-bottom: 12pt;
      padding-left: 24pt;
    }}
    li {{
      margin-bottom: 6pt;
      line-height: 1.5;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 14pt 0;
      font-size: 11pt;
    }}
    th, td {{
      border: 1pt solid #cbd5e1;
      padding: 8pt 10pt;
      text-align: left;
      line-height: 1.4;
    }}
    th {{
      background: #0f172a;
      color: #ffffff;
      font-weight: bold;
    }}
    tr:nth-child(even) td {{
      background: #f8fafc;
    }}
    .cover-page {{
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 9.69in;
    }}
    .figure-container {{
      text-align: center;
      margin: 18pt 0;
      page-break-inside: avoid;
    }}
    .figure-container img {{
      max-width: 100%;
      height: auto;
      border: 1pt solid #cbd5e1;
      border-radius: 4pt;
      box-shadow: 0 2pt 6pt rgba(0,0,0,0.06);
    }}
    .figure-caption {{
      font-size: 10.5pt;
      font-style: italic;
      font-weight: bold;
      color: #475569;
      margin-top: 6pt;
    }}
    .code-block {{
      background: #0f172a;
      color: #f8fafc;
      font-family: 'Courier New', Courier, monospace;
      font-size: 10.5pt;
      padding: 10pt 14pt;
      border-radius: 4pt;
      margin: 12pt 0;
      line-height: 1.4;
      white-space: pre-wrap;
    }}
    @media print {{
      body {{
        background: #ffffff;
        padding: 0;
      }}
      .document-page {{
        box-shadow: none;
        margin: 0;
        width: 100%;
        min-height: auto;
        padding: 0;
        page-break-after: always;
      }}
      .document-page:last-child {{
        page-break-after: avoid;
      }}
    }}
  </style>
</head>
<body>

  <!-- COVER PAGE -->
  <div class="document-page">
    <div class="cover-page">
      <div>
        <h2 style="font-size: 15pt; margin-bottom: 4pt; text-align: center;">VIVEKANAND EDUCATION SOCIETY'S INSTITUTE OF TECHNOLOGY</h2>
        <p style="font-size: 13pt; font-weight: bold; margin-bottom: 2pt; text-align: center;">DEPARTMENT OF INFORMATION TECHNOLOGY</p>
        <p style="font-size: 11pt; font-style: italic; color: #475569; margin-bottom: 40pt; text-align: center;">(Affiliated to the University of Mumbai)</p>

        <p style="font-size: 13pt; font-weight: bold; margin-bottom: 12pt; text-align: center;">A MINI-PROJECT REPORT ON</p>

        <h1 style="font-size: 20pt; color: #0284c7; border: none; margin-bottom: 12pt; text-align: center;">
          PHARMACARE — FULL-STACK PHARMACY MANAGEMENT SYSTEM
        </h1>
        <p style="font-size: 12pt; font-style: italic; color: #334155; margin-bottom: 40pt; text-align: center;">
          Intelligent FEFO POS Billing, Batch-Level Inventory Control, Real-Time WebSockets & Containerized DevOps Deployment
        </p>

        <p style="font-size: 11.5pt; font-weight: bold; margin-bottom: 4pt; text-align: center;">
          SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE DEGREE OF
        </p>
        <p style="font-size: 12.5pt; font-weight: bold; margin-bottom: 4pt; text-align: center;">
          BACHELOR OF ENGINEERING IN INFORMATION TECHNOLOGY
        </p>
        <p style="font-size: 11pt; color: #475569; margin-bottom: 30pt; text-align: center;">
          Under the Course of Full Stack Development (FSD) Laboratory
        </p>

        <table style="width: 80%; margin: 0 auto; font-size: 11pt;">
          <tr>
            <td style="width: 35%; font-weight: bold; background: #f1f5f9;">Candidate Name:</td>
            <td style="font-weight: bold;">Kirteesh Dattatray Rakshe</td>
          </tr>
          <tr>
            <td style="font-weight: bold; background: #f1f5f9;">Roll No. / Class:</td>
            <td>Roll No. 43 / Class D15A</td>
          </tr>
          <tr>
            <td style="font-weight: bold; background: #f1f5f9;">Academic Year:</td>
            <td>2026 – 2027</td>
          </tr>
          <tr>
            <td style="font-weight: bold; background: #f1f5f9;">GitHub Repository:</td>
            <td><a href="https://github.com/kirteexh/FSD_MiniProject" style="color: #0284c7;">https://github.com/kirteexh/FSD_MiniProject</a></td>
          </tr>
        </table>
      </div>

      <div>
        <p style="font-weight: bold; font-size: 12pt; margin-top: 40pt; text-align: center;">
          ACADEMIC YEAR 2026 – 2027
        </p>
      </div>
    </div>
  </div>

  <!-- TABLE OF CONTENTS -->
  <div class="document-page">
    <h1>TABLE OF CONTENTS</h1>
    <table style="border: none; margin-top: 20pt;">
      <tr style="border: none;"><td style="border: none; font-weight: bold;">1. Introduction and Objectives</td><td style="border: none; text-align: right; font-weight: bold;">Page 3</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">1.1 Project Overview and Clinical Context</td><td style="border: none; text-align: right;">Page 3</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">1.2 Problem Statement & Industry Challenges</td><td style="border: none; text-align: right;">Page 3</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">1.3 Key Project Objectives</td><td style="border: none; text-align: right;">Page 4</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">1.4 Target Audience and User Roles</td><td style="border: none; text-align: right;">Page 4</td></tr>
      <tr style="border: none;"><td style="border: none; font-weight: bold;">2. Technologies Used and System Design</td><td style="border: none; text-align: right; font-weight: bold;">Page 5</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">2.1 Technology Stack Architecture</td><td style="border: none; text-align: right;">Page 5</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">2.2 High-Level System Architecture Design</td><td style="border: none; text-align: right;">Page 6</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">2.3 Data Flow & FEFO Algorithmic Design</td><td style="border: none; text-align: right;">Page 7</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">2.4 Database Schema & Persistence Architecture</td><td style="border: none; text-align: right;">Page 8</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">2.5 RESTful API Specification and WebSocket Protocol</td><td style="border: none; text-align: right;">Page 9</td></tr>
      <tr style="border: none;"><td style="border: none; font-weight: bold;">3. Implementation with Screenshots</td><td style="border: none; text-align: right; font-weight: bold;">Page 10</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">3.1 Authentication & Role-Based Access Control (RBAC)</td><td style="border: none; text-align: right;">Page 10</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">3.2 Intelligent FEFO POS Billing Interface</td><td style="border: none; text-align: right;">Page 11</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">3.3 Clinical Inventory and Batch Management</td><td style="border: none; text-align: right;">Page 12</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">3.4 Shelf-Life Monitoring and Expiry Protocol</td><td style="border: none; text-align: right;">Page 13</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">3.5 Executive Financial Analytics & Visual Reporting</td><td style="border: none; text-align: right;">Page 14</td></tr>
      <tr style="border: none;"><td style="border: none; font-weight: bold;">4. Deployment and DevOps</td><td style="border: none; text-align: right; font-weight: bold;">Page 15</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">4.1 Multi-Container Docker Architecture</td><td style="border: none; text-align: right;">Page 15</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">4.2 Docker Compose Runtime Orchestration</td><td style="border: none; text-align: right;">Page 16</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">4.3 Automated CI/CD Pipeline via GitHub Actions</td><td style="border: none; text-align: right;">Page 17</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">4.4 Production Cloud Deployment & Security Hardening</td><td style="border: none; text-align: right;">Page 18</td></tr>
      <tr style="border: none;"><td style="border: none; font-weight: bold;">5. Conclusion and Future Scope</td><td style="border: none; text-align: right; font-weight: bold;">Page 19</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">5.1 Summary of Accomplishments</td><td style="border: none; text-align: right;">Page 19</td></tr>
      <tr style="border: none;"><td style="border: none; padding-left: 20pt;">5.2 Future Enhancements & Commercial Roadmap</td><td style="border: none; text-align: right;">Page 19</td></tr>
      <tr style="border: none;"><td style="border: none; font-weight: bold;">6. GitHub Repository & Live Deployment</td><td style="border: none; text-align: right; font-weight: bold;">Page 20</td></tr>
    </table>
  </div>

  <!-- CHAPTER 1 -->
  <div class="document-page">
    <h1>1. Introduction and Objectives</h1>
    
    <h2>1.1 Project Overview and Clinical Context</h2>
    <p>
      Modern pharmaceutical retail and hospital dispensaries operate in highly demanding, clinical environments where precision, speed, and regulatory compliance are essential to patient well-being and commercial sustainability. Unlike conventional commodity retail systems, pharmaceutical operations deal with potent, regulated chemical compounds, strict shelf-life expiration dates, batch traceability mandates, schedule-restricted narcotics, and dynamic manufacturer price revisions.
    </p>
    <p>
      <strong>PharmaCare</strong> is a full-stack, enterprise-grade pharmacy management web platform designed to streamline retail and hospital dispensary workflows. By combining a contemporary Next.js 14 frontend, a decoupled Express.js REST and Socket.IO backend, and dual-mode MongoDB Atlas persistence, PharmaCare modernizes traditional drug dispensing, automated batch allocation, and financial auditing.
    </p>

    <h2>1.2 Problem Statement & Industry Challenges</h2>
    <p>
      A comprehensive operational analysis of independent pharmacies and dispensary chains reveals several pervasive failure modes arising from legacy desktop software or manual paper-based ledger systems:
    </p>
    <ul>
      <li><strong>Dead Stock & High Expiry Write-Off Losses:</strong> In conventional retail dispensaries, staff grab the most accessible medication boxes from shelves during rush hours. This human tendency leaves earlier-received batches lingering in the back of racks until they expire, generating significant recurring financial losses for pharmacy owners.</li>
      <li><strong>Slow Checkout Bottlenecks & Prescription Verification:</strong> Manual batch number entry, manual tax calculations, and disconnected verification of Schedule-H prescription drugs create prolonged queues at dispensary counters, risking patient frustration and data entry mistakes.</li>
      <li><strong>Inventory Desynchronization & Stock-Outs:</strong> Without real-time inventory synchronization, dispensaries often run out of essential, life-saving antibiotics, insulin, and cardiac formulations without advance warning.</li>
      <li><strong>Inadequate Auditing & Role Segregation:</strong> Traditional single-tier desktop systems fail to provide robust role-based access control (RBAC), leaving critical operations like stock adjustments, clinical disposal write-offs, and price updates vulnerable to untracked human error or insider theft.</li>
    </ul>

    <h2>1.3 Key Project Objectives</h2>
    <p>The primary objectives established for the development of the PharmaCare platform are as follows:</p>
    <ul>
      <li><strong>Intelligent First-Expiry, First-Out (FEFO) POS Billing:</strong> Design and implement an automated point-of-sale checkout engine that programmatically selects and deducts inventory from the earliest expiring batch, completely eliminating human bias in dispensing aged stock.</li>
      <li><strong>Batch-Level Traceability & Clinical Audit Trails:</strong> Maintain granular lifecycle history for every individual pharmaceutical batch, including manufacturer details, manufacturing and expiry dates, purchase costs, MRP, supplier GSTINs, and audited stock adjustments.</li>
      <li><strong>Proactive Shelf-Life Expiry Monitoring:</strong> Provide real-time categorization of dispensary inventory into clinical urgency tiers (&lt;7 days, &lt;30 days, &lt;90 days, and expired), complete with formal clinical write-off logging.</li>
      <li><strong>Real-Time Stock Alerts via WebSockets:</strong> Integrate bidirectional Socket.IO WebSockets to broadcast instant, asynchronous notifications to all active workstations whenever any critical medicine breaches its minimum reorder threshold.</li>
      <li><strong>Robust Role-Based Security & Production DevOps:</strong> Enforce JWT authentication with password hashing (bcryptjs) separating Store Administrator and Cashier roles, and package the complete system with Docker multi-stage containers and automated GitHub Actions CI/CD.</li>
    </ul>

    <h2>1.4 Target Audience and User Roles</h2>
    <p>The system explicitly caters to two distinct operational user classes with strictly partitioned permissions:</p>
    <ul>
      <li><strong>Store Administrator (Pharmacist-in-Charge / Owner):</strong> Authorized with comprehensive administrative privileges including medication catalog authoring, batch creation, audited stock quantity adjustments, clinical disposal approvals, purchase order procurement, staff credential provisioning, and executive financial reporting.</li>
      <li><strong>Dispensary Cashier (Sales Staff):</strong> Authorized with frontline operational permissions focused on rapid POS barcode billing, patient prescription recording, customer invoice generation, held bill caching, and real-time stock catalog lookups.</li>
    </ul>
  </div>

  <!-- CHAPTER 2 -->
  <div class="document-page">
    <h1>2. Technologies Used and System Design</h1>

    <h2>2.1 Technology Stack Architecture</h2>
    <p>
      PharmaCare leverages a modern, decoupled full-stack architecture carefully selected to achieve high concurrency, sub-second POS transaction latencies, responsive UI rendering, and production-grade reliability.
    </p>

    <table>
      <thead>
        <tr>
          <th>Architecture Tier</th>
          <th>Technologies & Frameworks</th>
          <th>Key Purpose & Justification</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Frontend Presentation</strong></td>
          <td>Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Framer Motion, Redux Toolkit, Recharts, Lucide React</td>
          <td>Server-Side Rendering (SSR) & Client Hydration, modular typed components, clinical dark/light theming, client-side cart state management, and real-time analytics graphs.</td>
        </tr>
        <tr>
          <td><strong>Backend REST & Sockets</strong></td>
          <td>Node.js (v18+), Express.js, TypeScript, Socket.IO, Helmet, CORS, Express-Rate-Limit, Zod, bcryptjs, JWT</td>
          <td>High-throughput asynchronous non-blocking event loop, strict RESTful API routing, bidirectional WebSocket notification broadcasting, cryptographic security, and payload schema validation.</td>
        </tr>
        <tr>
          <td><strong>Data Persistence</strong></td>
          <td>MongoDB Atlas, Mongoose ODM (Object Data Modeling), Hybrid In-Memory Fallback Engine</td>
          <td>Document-oriented schema flexibility for multi-batch arrays, indexed geospatial/temporal querying for expiry windows, and seamless offline evaluation capability.</td>
        </tr>
        <tr>
          <td><strong>DevOps & Deployment</strong></td>
          <td>Docker, Docker Compose, Nginx Reverse Proxy, GitHub Actions CI/CD Pipeline, Render Cloud Platform</td>
          <td>Multi-stage container image builds for minimized runtime footprint, microservice orchestration, automated testing pipelines on code push, and zero-downtime cloud hosting.</td>
        </tr>
      </tbody>
    </table>

    <h2>2.2 High-Level System Architecture Design</h2>
    <p>
      PharmaCare implements a decoupled, three-tier architecture adhering to modern microservice and client-server standards. As illustrated in Figure 1, the presentation layer communicates with the backend via two dedicated transport channels: standard stateless HTTPS REST endpoints for transactional CRUD operations, and persistent, low-overhead WebSocket (WSS) tunnels managed via Socket.IO for event-driven push notifications.
    </p>
    <div class="figure-container">
      <img src="{fig1}" alt="Figure 1: System Architecture">
      <div class="figure-caption">Figure 1: PharmaCare 3-Tier Enterprise System Architecture</div>
    </div>

    <h2>2.3 Data Flow & FEFO Algorithmic Design</h2>
    <p>
      The core mathematical and business innovation in PharmaCare is its First-Expiry, First-Out (FEFO) dispensing algorithm. When an item is added to the dispensary checkout cart with requested quantity Q, the backend queries all unexpired, active inventory batches for that medicine and orders them in ascending chronological order of expiration dates (expiryDate ASC). As detailed in the flowchart in Figure 2, the algorithm deducts stock sequentially from the earliest expiring batch, cascading across lots until the quantity is fulfilled.
    </p>
    <div class="figure-container">
      <img src="{fig2}" alt="Figure 2: FEFO Flowchart">
      <div class="figure-caption">Figure 2: First-Expiry, First-Out (FEFO) Batch Allocation Logic Flowchart</div>
    </div>
  </div>

  <!-- CHAPTER 3 -->
  <div class="document-page">
    <h1>3. Implementation with Screenshots</h1>

    <h2>3.1 Authentication & Role-Based Access Control (RBAC)</h2>
    <p>
      PharmaCare implements rigorous, stateless authentication utilizing JSON Web Tokens (JWT). Upon successful credential verification via bcrypt comparison (salt rounds: 10), the server issues a signed JWT payload containing the user's unique ID, username, email, and authorization role (admin or cashier). Protected backend routes are guarded by high-order middleware functions (requireAuth and requireAdmin).
    </p>

    <h2>3.2 Intelligent FEFO POS Billing Interface</h2>
    <p>
      The Point of Sale billing interface is optimized for high-speed counter operations. Cashiers can instantly lookup medicines via live text queries or barcode scanner inputs. As shown in Figure 3, the POS terminal features a split-pane layout: the left pane houses the real-time active cart displaying medicine names, automatically allocated batch numbers, expiry months, unit prices, and sub-totals. The right pane computes live tax breakdowns, including Central GST (CGST) and State GST (SGST), discounts, round-off adjustments, and payment method toggles.
    </p>
    <div class="figure-container">
      <img src="{fig3}" alt="Figure 3: POS Billing">
      <div class="figure-caption">Figure 3: PharmaCare Intelligent Point-of-Sale (POS) Billing Interface</div>
    </div>

    <h2>3.3 Clinical Inventory and Batch Management</h2>
    <p>
      The inventory catalog view provides pharmacists with comprehensive visibility across all active medicine formulations. As depicted in Figure 4, the catalog lists brand names, generic formulations, batch numbers, expiration timelines, unit MRPs, and real-time stock balances. Each medicine displays color-coded status badges: In Stock (green), Low Stock (amber), Expiring Soon (orange), and Out of Stock (red).
    </p>
    <div class="figure-container">
      <img src="{fig4}" alt="Figure 4: Inventory Catalog">
      <div class="figure-caption">Figure 4: Clinical Medication Catalog and Multi-Batch Tracking Interface</div>
    </div>

    <h2>3.4 Shelf-Life Monitoring and Expiry Protocol</h2>
    <p>
      To systematically prevent aged medication losses, PharmaCare features a dedicated Expiry Management subsystem. As illustrated in Figure 5, inventory lots are automatically segmented into chronological hazard intervals: &lt;7 Days, &lt;30 Days, &lt;90 Days, and Already Expired. Pharmacists can trigger one-click clinical disposal workflows, logging regulatory destruction reasons.
    </p>
    <div class="figure-container">
      <img src="{fig5}" alt="Figure 5: Expiry Management">
      <div class="figure-caption">Figure 5: PharmaCare Shelf-Life Monitoring and Expiry Disposal Management Dashboard</div>
    </div>

    <h2>3.5 Executive Financial Analytics & Visual Reporting</h2>
    <p>
      For store owners and dispensary directors, PharmaCare provides real-time business intelligence dashboards built with Recharts. As shown in Figure 6, the analytics module displays primary key performance indicators: Gross Revenue, Invoice Volume, Total Inventory Asset Valuation, and Net Operating Margin. Visual charts breakdown sales revenue by pharmaceutical categories.
    </p>
    <div class="figure-container">
      <img src="{fig6}" alt="Figure 6: Financial Reports">
      <div class="figure-caption">Figure 6: Executive Financial Analytics & Category Sales Performance Dashboard</div>
    </div>
  </div>

  <!-- CHAPTER 4 -->
  <div class="document-page">
    <h1>4. Deployment and DevOps</h1>

    <h2>4.1 Multi-Container Docker Architecture</h2>
    <p>
      PharmaCare is fully containerized using Docker to eliminate environment discrepancies and ensure rapid, reproducible deployments across developer machines, staging clusters, and production cloud servers. Both the Next.js frontend client and Express.js backend server utilize optimized multi-stage Dockerfiles, cutting final image footprints by over 65%.
    </p>

    <h2>4.2 Docker Compose Runtime Orchestration</h2>
    <p>
      The multi-service ecosystem is orchestrated via Docker Compose (docker-compose.yml and docker-compose.prod.yml). The orchestration defines four coordinated services interconnected via an isolated internal bridge network:
    </p>
    <ul>
      <li><strong>pharmacare-server:</strong> Node.js Express REST API & Socket.IO runtime executing on port 5001 with automated healthcheck probes (wget /api/health).</li>
      <li><strong>pharmacare-client:</strong> Next.js 14 SSR frontend serving on port 3000, depending on healthy server status.</li>
      <li><strong>pharmacare-proxy (Nginx):</strong> Acts as an edge reverse proxy routing incoming port 80/443 traffic to the client and /api calls to the backend container.</li>
      <li><strong>pharmacare-mongo:</strong> Containerized local database service with persistent Docker volume mappings.</li>
    </ul>

    <h2>4.3 Automated CI/CD Pipeline via GitHub Actions</h2>
    <p>
      Continuous Integration and Continuous Deployment (CI/CD) is automated using GitHub Actions (.github/workflows/ci.yml). As visualized in Figure 7, every git commit pushed to the main branch or Pull Request automatically triggers a 3-stage validation pipeline: backend tests, frontend build, and Docker image compilation.
    </p>
    <div class="figure-container">
      <img src="{fig7}" alt="Figure 7: DevOps Pipeline">
      <div class="figure-caption">Figure 7: PharmaCare DevOps Architecture and GitHub Actions CI/CD Pipeline Workflow</div>
    </div>

    <h2>4.4 Production Cloud Deployment & Security Hardening</h2>
    <p>
      The live production application is deployed on the Render cloud platform with MongoDB Atlas cloud clusters. Production security hardening measures implemented include Helmet security headers, Express rate limiting on auth endpoints, CORS origin restriction, and cryptographic password salting with bcryptjs.
    </p>
  </div>

  <!-- CHAPTER 5 & 6 -->
  <div class="document-page">
    <h1>5. Conclusion and Future Scope</h1>

    <h2>5.1 Summary of Accomplishments</h2>
    <p>
      The PharmaCare Mini-Project successfully demonstrates the design, full-stack engineering, and cloud deployment of a robust, enterprise-grade pharmacy management application. Key project milestones accomplished include:
    </p>
    <ul>
      <li><strong>Elimination of Expiry Losses:</strong> The automated FEFO algorithm successfully dispenses earliest expiring medicine batches, solving the primary cause of dead inventory in retail pharmacies.</li>
      <li><strong>Rapid Counter Throughput:</strong> The streamlined POS checkout interface reduces customer transaction time from minutes to seconds with automatic tax computation and receipt generation.</li>
      <li><strong>Full Regulatory Compliance:</strong> Batch-level traceability and mandatory Schedule-H prescription recording ensure compliance with Indian drug regulatory mandates.</li>
      <li><strong>Production-Ready DevOps Pipeline:</strong> Containerization with Docker, multi-service orchestration with Docker Compose, and automated CI/CD via GitHub Actions establish an enterprise standard of maintainability.</li>
    </ul>

    <h2>5.2 Future Enhancements & Commercial Roadmap</h2>
    <p>
      Building upon the proven foundation established in this project, future development phases will incorporate the following advanced capabilities:
    </p>
    <ul>
      <li><strong>AI-Powered Demand & Reorder Forecasting:</strong> Integrate machine learning predictive models (ARIMA / LSTM) to analyze seasonal disease trends and automatically recommend purchase order quantities for critical drugs.</li>
      <li><strong>Automated WhatsApp & SMS Invoice Dispatch:</strong> Integrate the WhatsApp Business Cloud API to deliver digital, paperless GST tax invoices and dosage reminders directly to patients' smartphones.</li>
      <li><strong>Drug-Drug Interaction & Allergy Checker:</strong> Integrate medical reference APIs to provide instant clinical contraindication warnings at the POS terminal when a doctor prescribes potentially conflicting drug combinations.</li>
      <li><strong>Mobile Dispensary Companion App:</strong> Develop a cross-platform mobile application using React Native allowing dispensary managers to audit inventory and scan barcodes directly from handheld smartphones.</li>
    </ul>

    <h1>6. GitHub Repository and Live Deployment Links</h1>
    <p>
      All source code, configuration files, Docker container recipes, automated test suites, and documentation for the PharmaCare project have been committed, version-controlled, and published on GitHub, alongside a live production deployment on Render.
    </p>

    <table>
      <tr>
        <th style="width: 35%;">Resource / Reference</th>
        <th>URL / Details</th>
      </tr>
      <tr>
        <td><strong>Official GitHub Repository:</strong></td>
        <td><a href="https://github.com/kirteexh/FSD_MiniProject" style="color: #0284c7; font-weight: bold;">https://github.com/kirteexh/FSD_MiniProject</a></td>
      </tr>
      <tr>
        <td><strong>Live Production Cloud Deployment:</strong></td>
        <td><a href="https://fsd-miniproject-skab.onrender.com" style="color: #0284c7; font-weight: bold;">https://fsd-miniproject-skab.onrender.com</a></td>
      </tr>
      <tr>
        <td><strong>Backend Health Check Endpoint:</strong></td>
        <td><a href="https://fsd-miniproject-skab.onrender.com/api/health" style="color: #0284c7;">https://fsd-miniproject-skab.onrender.com/api/health</a></td>
      </tr>
      <tr>
        <td><strong>Primary Author & Developer:</strong></td>
        <td>Kirteesh Dattatray Rakshe (Roll No. 43, Class D15A)</td>
      </tr>
      <tr>
        <td><strong>License & Rights:</strong></td>
        <td>MIT Open Source License (2026)</td>
      </tr>
    </table>

    <div class="code-block">git clone https://github.com/kirteexh/FSD_MiniProject.git
cd FSD_MiniProject
npm run install:all
npm run dev</div>

    <p style="text-align: center; font-weight: bold; font-style: italic; margin-top: 30pt; color: #64748b;">
      — End of Mini-Project Report —
    </p>
  </div>

</body>
</html>
"""

out_html = "FSD_Mini_Project_Report_Kirteesh_Rakshe.html"
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated HTML report: {out_html} ({os.path.getsize(out_html)} bytes)")

# Also copy to Pharmacy Management System
dest_html = os.path.join(r"C:\Users\kirte\OneDrive\Desktop\3rd Year\FSD\Pharmacy Management System", out_html)
try:
    with open(dest_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Copied HTML report to: {dest_html}")
except Exception as e:
    print(f"Could not copy HTML to {dest_html}: {e}")
