import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:5000/api';

// Minimalist clean SVG icons
const ShieldIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  </svg>
);

const LockIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
  </svg>
);

const UnlockIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
    <path d="M7 11V7a5 5 0 0 1 9.9-1"/>
  </svg>
);

const TerminalIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="4 17 10 11 4 5"/>
    <line x1="12" y1="19" x2="20" y2="19"/>
  </svg>
);

const CopyIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
  </svg>
);

const CheckIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12"/>
  </svg>
);

const SendIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"/>
    <polygon points="22 2 15 22 11 13 2 9 22 2"/>
  </svg>
);

const AlertTriangleIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
    <line x1="12" y1="9" x2="12" y2="13"/>
    <line x1="12" y1="17" x2="12.01" y2="17"/>
  </svg>
);

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('jwt_token') || '');
  const [profile, setProfile] = useState(null);
  const [securityMode, setSecurityMode] = useState('vulnerable');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // IDOR Simulator state
  const [simulatedId, setSimulatedId] = useState('102');
  const [simResult, setSimResult] = useState(null);
  const [simLoading, setSimLoading] = useState(false);
  const [copiedToken, setCopiedToken] = useState(false);

  useEffect(() => {
    fetchSecurityMode();
    const storedUser = localStorage.getItem('user_info');
    if (storedUser && token) {
      const parsed = JSON.parse(storedUser);
      setCurrentUser(parsed);
      fetchProfile(parsed.id, token);
    } else {
      loginUser('asha@test.com', 'password123');
    }
  }, []);

  const fetchSecurityMode = async () => {
    try {
      const res = await fetch(`${API_BASE}/security-status`);
      const data = await res.json();
      setSecurityMode(data.securityMode);
    } catch (err) {
      console.error('Failed to get security status', err);
    }
  };

  const toggleSecurityMode = async () => {
    const nextMode = securityMode === 'vulnerable' ? 'secure' : 'vulnerable';
    try {
      const res = await fetch(`${API_BASE}/security-mode`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: nextMode })
      });
      const data = await res.json();
      setSecurityMode(data.securityMode);
      if (token) {
        runIdorSimulator(simulatedId, token);
      }
    } catch (err) {
      console.error('Error toggling security mode', err);
    }
  };

  const loginUser = async (email, password) => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Authentication failed');

      setToken(data.token);
      setCurrentUser(data.user);
      localStorage.setItem('jwt_token', data.token);
      localStorage.setItem('user_info', JSON.stringify(data.user));

      await fetchProfile(data.user.id, data.token);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchProfile = async (id, authToken) => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/profiles/${id}`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || `HTTP ${res.status}: Access Denied`);
      }
      setProfile(data);
    } catch (err) {
      setError(err.message);
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setToken('');
    setProfile(null);
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_info');
  };

  const runIdorSimulator = async (targetId, testToken) => {
    setSimLoading(true);
    setSimResult(null);
    const useToken = testToken || token;
    try {
      const startTime = performance.now();
      const res = await fetch(`${API_BASE}/profiles/${targetId}`, {
        headers: {
          'Authorization': `Bearer ${useToken}`
        }
      });
      const duration = Math.round(performance.now() - startTime);
      const data = await res.json();

      setSimResult({
        status: res.status,
        statusText: res.statusText,
        duration: `${duration} ms`,
        targetId,
        tokenUser: currentUser?.name || 'User A',
        data
      });
    } catch (err) {
      setSimResult({
        status: 500,
        statusText: 'Internal Error',
        error: err.message
      });
    } finally {
      setSimLoading(false);
    }
  };

  const copyToken = () => {
    if (!token) return;
    navigator.clipboard.writeText(token);
    setCopiedToken(true);
    setTimeout(() => setCopiedToken(false), 2000);
  };

  const getInitials = (name) => {
    if (!name) return 'US';
    const parts = name.split(' ');
    return parts.length >= 2 ? `${parts[0][0]}${parts[1][0]}` : name.substring(0, 2).toUpperCase();
  };

  return (
    <div className="app-viewport">
      {/* Sleek Top Navigation */}
      <nav className="navbar">
        <div className="nav-brand">
          <div className="brand-icon">
            <ShieldIcon style={{ width: 18, height: 18 }} />
          </div>
          <div className="brand-meta">
            <div className="brand-title">
              Aegis Security Lab
              <span className="brand-tag">IDOR Audit</span>
            </div>
            <div className="brand-sub">Full Stack Security Assessment Suite</div>
          </div>
        </div>

        <div className="nav-actions">
          {currentUser && (
            <div className="user-session-chip">
              <div className="user-avatar-mini">{getInitials(currentUser.name)}</div>
              <span style={{ color: '#f8fafc', fontWeight: 500 }}>{currentUser.name}</span>
              <span style={{ color: '#64748b' }}>({currentUser.email})</span>
            </div>
          )}
          {currentUser && (
            <button onClick={handleLogout} className="btn btn-sm">
              Sign Out
            </button>
          )}
        </div>
      </nav>

      {/* Main Container */}
      <main className="content-wrapper">
        {/* Security Control Banner */}
        <section className={`security-header-banner ${securityMode}`}>
          <div className="banner-left">
            <span className={`banner-badge ${securityMode}`}>
              <span className="pulse-dot"></span>
              {securityMode === 'vulnerable' ? 'Vulnerable (Direct Reference)' : 'Remediated (Ownership Enforced)'}
            </span>
            <div>
              <div className="banner-title">
                Active Policy: {securityMode === 'vulnerable' ? 'Insecure Object Lookup' : 'Strict Subject-Resource Authorization'}
              </div>
              <div className="banner-desc">
                {securityMode === 'vulnerable'
                  ? 'Server retrieves profile by parameter ID without checking caller ownership (Step 6 vulnerability).'
                  : 'Server strictly validates that req.user.id equals profile.userId before granting access (Step 7 fix).'}
              </div>
            </div>
          </div>

          <button onClick={toggleSecurityMode} className="btn btn-toggle">
            {securityMode === 'vulnerable' ? (
              <>
                <ShieldIcon style={{ width: 14, height: 14, color: '#10b981' }} />
                Enable Ownership Check (Remediation)
              </>
            ) : (
              <>
                <UnlockIcon style={{ width: 14, height: 14, color: '#f43f5e' }} />
                Revert to Vulnerable Mode
              </>
            )}
          </button>
        </section>

        {/* Persona Switcher */}
        <section className="account-switcher-grid">
          <div
            onClick={() => loginUser('asha@test.com', 'password123')}
            className={`account-card ${currentUser?.id === '101' ? 'active' : ''}`}
          >
            <div className="avatar-large">AT</div>
            <div className="account-details">
              <div className="account-name-row">
                <span className="account-name">User A &mdash; Asha Test</span>
                <span className="account-id-badge">ID: 101</span>
              </div>
              <div className="account-subtext">HR Specialist &bull; asha@test.com</div>
            </div>
          </div>

          <div
            onClick={() => loginUser('bala@test.com', 'password123')}
            className={`account-card ${currentUser?.id === '102' ? 'active' : ''}`}
          >
            <div className="avatar-large">BT</div>
            <div className="account-details">
              <div className="account-name-row">
                <span className="account-name">User B &mdash; Bala Test</span>
                <span className="account-id-badge">ID: 102</span>
              </div>
              <div className="account-subtext">Senior Finance Officer &bull; bala@test.com</div>
            </div>
          </div>
        </section>

        {/* Dashboard Grid */}
        <div className="dashboard-grid">
          {/* Left Panel: Profile Record */}
          <section className="card-panel">
            <div className="card-header">
              <div className="card-title-group">
                <ShieldIcon className="card-title-icon" />
                <span className="card-title">Personnel Identity Record</span>
              </div>
              {profile && (
                <span className="mono" style={{ fontSize: '11px', color: '#64748b' }}>
                  REF // {profile._id}
                </span>
              )}
            </div>

            <div className="card-body">
              {profile ? (
                <>
                  <div className="profile-hero">
                    <div className="hero-avatar">{getInitials(profile.name)}</div>
                    <div className="hero-info">
                      <h2>{profile.name}</h2>
                      <p>{profile.designation} &bull; {profile.department}</p>
                    </div>
                  </div>

                  <div className="profile-field-list">
                    <div className="profile-field-row">
                      <span className="field-label">Resource ID</span>
                      <span className="field-value mono highlight">{profile._id}</span>
                    </div>
                    <div className="profile-field-row">
                      <span className="field-label">Corporate Email</span>
                      <span className="field-value">{profile.email}</span>
                    </div>
                    <div className="profile-field-row">
                      <span className="field-label">Direct Line</span>
                      <span className="field-value">{profile.phone}</span>
                    </div>
                    <div className="profile-field-row">
                      <span className="field-label">Business Unit</span>
                      <span className="field-value">{profile.department}</span>
                    </div>
                    <div className="profile-field-row">
                      <span className="field-label">Work Location</span>
                      <span className="field-value">{profile.address}</span>
                    </div>
                    <div className="profile-field-row">
                      <span className="field-label">Annual Base</span>
                      <span className="field-value">
                        <span className="compensation-pill">{profile.accountBalance}</span>
                      </span>
                    </div>
                  </div>

                  <div className="classified-box">
                    <div className="classified-header">
                      <LockIcon style={{ width: 13, height: 13 }} />
                      Restricted Confidential Personnel Record
                    </div>
                    <div className="classified-text">{profile.confidentialNotes}</div>
                  </div>

                  <div className="endpoint-hint-box">
                    <span style={{ color: '#94a3b8' }}>Live Profile Endpoint:</span>
                    <span className="endpoint-badge">GET /api/profiles/{profile._id}</span>
                  </div>
                </>
              ) : (
                <div style={{ textAlign: 'center', padding: '40px 0', color: '#64748b' }}>
                  Select an account above to load profile records.
                </div>
              )}
            </div>
          </section>

          {/* Right Panel: API Security & IDOR Console */}
          <section className="card-panel">
            <div className="card-header">
              <div className="card-title-group">
                <TerminalIcon className="card-title-icon" />
                <span className="card-title">API Audit &amp; IDOR Console</span>
              </div>
              <span className="mono" style={{ fontSize: '11px', color: '#64748b' }}>
                POSTMAN SIMULATOR
              </span>
            </div>

            <div className="card-body">
              {/* Token Inspector Bar */}
              <div className="console-section-label">
                <span>Active Bearer Token ({currentUser?.name})</span>
                <button onClick={copyToken} className="btn btn-sm">
                  {copiedToken ? (
                    <>
                      <CheckIcon style={{ width: 12, height: 12, color: '#34d399' }} />
                      Token Copied
                    </>
                  ) : (
                    <>
                      <CopyIcon style={{ width: 12, height: 12 }} />
                      Copy for Postman
                    </>
                  )}
                </button>
              </div>

              <div className="token-viewer-bar">
                <span>{token ? `${token.substring(0, 38)}...[AUTHENTICATION TOKEN MASKED]` : 'No active token'}</span>
              </div>

              {/* URL Dispatcher */}
              <div className="console-section-label">
                <span>Target API Endpoint Request</span>
              </div>

              <div className="url-composer-bar">
                <div className="http-method">GET</div>
                <input
                  type="text"
                  className="url-input-field"
                  value={`http://localhost:5000/api/profiles/${simulatedId}`}
                  onChange={(e) => {
                    const parts = e.target.value.split('/api/profiles/');
                    if (parts[1] !== undefined) setSimulatedId(parts[1]);
                  }}
                />
                <button
                  onClick={() => runIdorSimulator(simulatedId, token)}
                  disabled={simLoading || !token}
                  className="send-trigger-btn"
                >
                  <SendIcon style={{ width: 13, height: 13 }} />
                  {simLoading ? 'Sending...' : 'Send'}
                </button>
              </div>

              {/* Quick Preset Buttons */}
              <div className="preset-actions-bar">
                <button
                  onClick={() => { setSimulatedId('101'); runIdorSimulator('101', token); }}
                  className="btn btn-sm"
                >
                  Test 101 (User A Self)
                </button>
                <button
                  onClick={() => { setSimulatedId('102'); runIdorSimulator('102', token); }}
                  className="btn btn-sm"
                  style={{ borderColor: 'rgba(244, 63, 94, 0.4)', color: '#fda4af' }}
                >
                  Test 102 (Cross-User Exploit)
                </button>
              </div>

              {/* Terminal Window */}
              {simResult && (
                <div className="terminal-window">
                  <div className="terminal-titlebar">
                    <div className="window-dots">
                      <span className="window-dot dot-red"></span>
                      <span className="window-dot dot-yellow"></span>
                      <span className="window-dot dot-green"></span>
                    </div>
                    <div className="terminal-meta">
                      <span className={`status-tag ${simResult.status === 200 ? 'ok' : 'denied'}`}>
                        HTTP {simResult.status} {simResult.statusText}
                      </span>
                      <span style={{ color: '#64748b' }}>{simResult.duration}</span>
                    </div>
                  </div>

                  <pre className="terminal-body">
                    {JSON.stringify(simResult.data, null, 2)}
                  </pre>
                </div>
              )}

              {/* Explanatory Security Finding */}
              {simResult && (
                <div>
                  {simResult.status === 200 && simResult.targetId === '102' && currentUser?.id === '101' && (
                    <div className="audit-alert-box danger">
                      <AlertTriangleIcon style={{ width: 18, height: 18, flexShrink: 0 }} />
                      <div>
                        <strong>CRITICAL: Insecure Direct Object Reference (IDOR) Detected</strong>
                        User A's session successfully retrieved User B's unredacted confidential payroll and banking details without authorization checks.
                      </div>
                    </div>
                  )}

                  {simResult.status === 403 && (
                    <div className="audit-alert-box success">
                      <ShieldIcon style={{ width: 18, height: 18, flexShrink: 0 }} />
                      <div>
                        <strong>DEFENSE VERIFIED: Cross-Tenant Access Prohibited (HTTP 403)</strong>
                        The server enforced ownership validation (<code>req.user.id === profile.userId</code>) and successfully blocked the unauthorized access attempt.
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Postman Procedure Summary */}
              <div className="postman-guide-box">
                <strong>Postman Execution Summary:</strong>
                <ol>
                  <li><strong>Step 4:</strong> Request <code>GET /api/profiles/101</code> with User A token &rarr; <code>200 OK</code>.</li>
                  <li><strong>Step 5 (Exploit):</strong> Request <code>GET /api/profiles/102</code> with User A token &rarr; <code>200 OK</code> (Vulnerable).</li>
                  <li><strong>Step 8 (Retest):</strong> Switch to Remediated Mode, re-send 102 &rarr; <code>403 Forbidden</code> (Access Denied).</li>
                </ol>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
