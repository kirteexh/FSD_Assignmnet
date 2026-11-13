import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:5000/api';

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

  return (
    <div className="app-wrapper">
      {/* Top Corporate Navigation */}
      <header className="top-header">
        <div className="brand">
          <div className="brand-mark">EP</div>
          <div className="brand-text">Enterprise Portal</div>
          <span className="brand-divider">/</span>
          <span className="brand-section">Access Control Assessment Lab</span>
        </div>

        <div className="header-user">
          {currentUser && (
            <div className="user-tag">
              Signed in as: <strong>{currentUser.name}</strong> ({currentUser.email})
            </div>
          )}
          {currentUser && (
            <button onClick={handleLogout} className="btn btn-sm">
              Sign Out
            </button>
          )}
        </div>
      </header>

      {/* Main Workspace */}
      <main className="main-container">
        {/* Security Controller Bar */}
        <section className="control-bar">
          <div className="control-info">
            <span className={`mode-badge ${securityMode}`}>
              {securityMode === 'vulnerable' ? 'Vulnerable' : 'Remediated'}
            </span>
            <div>
              <div className="control-title">
                Backend Routing Configuration: <strong>{securityMode === 'vulnerable' ? 'Unrestricted Direct Reference' : 'Strict Ownership Enforced'}</strong>
              </div>
              <div className="control-desc">
                {securityMode === 'vulnerable'
                  ? 'Endpoint /api/profiles/:id retrieves records without evaluating requester identity (Step 6 flaw).'
                  : 'Endpoint /api/profiles/:id verifies that req.user.id strictly matches profile.userId (Step 7 remediation).'}
              </div>
            </div>
          </div>

          <button onClick={toggleSecurityMode} className="btn">
            Switch to {securityMode === 'vulnerable' ? 'Remediated Mode (Enforce Auth)' : 'Vulnerable Mode (Baseline)'}
          </button>
        </section>

        {/* Account Persona Selector */}
        <nav className="account-bar" aria-label="Test Account Switcher">
          <button
            onClick={() => loginUser('asha@test.com', 'password123')}
            className={`account-tab ${currentUser?.id === '101' ? 'active' : ''}`}
          >
            <div className="account-tab-title">
              <span>User A &mdash; Asha Test</span>
              <span className="mono" style={{ fontSize: '11px', color: '#64748b' }}>ID: 101</span>
            </div>
            <div className="account-tab-meta">Role: HR Specialist &bull; asha@test.com</div>
          </button>

          <button
            onClick={() => loginUser('bala@test.com', 'password123')}
            className={`account-tab ${currentUser?.id === '102' ? 'active' : ''}`}
          >
            <div className="account-tab-title">
              <span>User B &mdash; Bala Test</span>
              <span className="mono" style={{ fontSize: '11px', color: '#64748b' }}>ID: 102</span>
            </div>
            <div className="account-tab-meta">Role: Senior Finance Officer &bull; bala@test.com</div>
          </button>
        </nav>

        {loading && <div style={{ fontSize: '13px', color: '#64748b', marginBottom: '14px' }}>Loading record...</div>}
        {error && <div style={{ fontSize: '13px', color: '#b91c1c', marginBottom: '14px' }}>Error: {error}</div>}

        {/* Two-Column Grid */}
        <div className="layout-grid">
          {/* Left Column: Personnel Record */}
          <section className="panel">
            <div className="panel-header">
              <span className="panel-title">Employee Profile Record</span>
              {profile && (
                <span className="mono" style={{ fontSize: '12px', color: '#64748b' }}>
                  Resource ID: {profile._id}
                </span>
              )}
            </div>

            <div className="panel-body">
              {profile ? (
                <>
                  <table className="field-table">
                    <tbody>
                      <tr>
                        <td className="field-label">Employee Name</td>
                        <td className="field-value">{profile.name}</td>
                      </tr>
                      <tr>
                        <td className="field-label">System Identifier</td>
                        <td className="field-value mono">{profile._id}</td>
                      </tr>
                      <tr>
                        <td className="field-label">Corporate Email</td>
                        <td className="field-value">{profile.email}</td>
                      </tr>
                      <tr>
                        <td className="field-label">Direct Contact</td>
                        <td className="field-value">{profile.phone}</td>
                      </tr>
                      <tr>
                        <td className="field-label">Business Unit</td>
                        <td className="field-value">{profile.department}</td>
                      </tr>
                      <tr>
                        <td className="field-label">Job Title</td>
                        <td className="field-value">{profile.designation}</td>
                      </tr>
                      <tr>
                        <td className="field-label">Work Location</td>
                        <td className="field-value">{profile.address}</td>
                      </tr>
                      <tr>
                        <td className="field-label">Base Compensation</td>
                        <td className="field-value mono">{profile.accountBalance}</td>
                      </tr>
                    </tbody>
                  </table>

                  <div className="sensitive-note">
                    <div className="sensitive-note-label">Restricted Internal Personnel Notes</div>
                    <div className="sensitive-note-text">{profile.confidentialNotes}</div>
                  </div>

                  <div className="notice-box">
                    <strong>Browser Network Inspection (Step 2 &amp; 3):</strong>
                    <div style={{ marginTop: '4px', fontFamily: 'monospace', fontSize: '11.5px', color: '#0369a1' }}>
                      GET http://localhost:5000/api/profiles/{profile._id}
                    </div>
                    <div style={{ marginTop: '2px', color: '#64748b' }}>
                      Status: 200 OK &bull; Authenticated via Bearer token in Request Headers.
                    </div>
                  </div>
                </>
              ) : (
                <div style={{ padding: '30px 0', textAlign: 'center', color: '#94a3b8', fontSize: '13px' }}>
                  No profile record loaded.
                </div>
              )}
            </div>
          </section>

          {/* Right Column: API Testing & IDOR Console */}
          <section className="panel">
            <div className="panel-header">
              <span className="panel-title">API Verification &amp; IDOR Console</span>
              <span style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase' }}>Steps 4, 5 &amp; 8</span>
            </div>

            <div className="panel-body">
              {/* Token Inspector */}
              <div className="console-row">
                <div className="console-label">
                  <span>Current Bearer Token ({currentUser?.name})</span>
                  <button onClick={copyToken} className="btn btn-sm">
                    {copiedToken ? 'Copied' : 'Copy for Postman'}
                  </button>
                </div>
                <div className="token-field">
                  <span>{token ? `${token.substring(0, 38)}...[Token Masked]` : 'No active token'}</span>
                </div>
              </div>

              {/* Request Builder */}
              <div className="console-row">
                <div className="console-label">
                  <span>API Request Dispatcher</span>
                </div>

                <div className="request-bar">
                  <span className="method-tag">GET</span>
                  <input
                    type="text"
                    className="url-box"
                    value={`http://localhost:5000/api/profiles/${simulatedId}`}
                    onChange={(e) => {
                      const parts = e.target.value.split('/api/profiles/');
                      if (parts[1] !== undefined) setSimulatedId(parts[1]);
                    }}
                  />
                  <button
                    onClick={() => runIdorSimulator(simulatedId, token)}
                    disabled={simLoading || !token}
                    className="btn btn-primary"
                    style={{ borderRadius: 0, border: 'none' }}
                  >
                    {simLoading ? 'Executing...' : 'Send'}
                  </button>
                </div>

                <div className="action-row">
                  <button
                    onClick={() => { setSimulatedId('101'); runIdorSimulator('101', token); }}
                    className="btn btn-sm"
                  >
                    Query ID: 101 (User A)
                  </button>
                  <button
                    onClick={() => { setSimulatedId('102'); runIdorSimulator('102', token); }}
                    className="btn btn-sm"
                  >
                    Query ID: 102 (Cross-User Exploit)
                  </button>
                </div>
              </div>

              {/* Response Inspector */}
              {simResult && (
                <div style={{ marginTop: '14px' }}>
                  <div className="response-header">
                    <span>
                      HTTP Status:{' '}
                      <span className={`response-status ${simResult.status === 200 ? 'ok' : 'denied'}`}>
                        {simResult.status} {simResult.statusText}
                      </span>
                    </span>
                    <span>Latency: {simResult.duration}</span>
                  </div>

                  <pre className="response-terminal">
                    {JSON.stringify(simResult.data, null, 2)}
                  </pre>

                  <div style={{ marginTop: '8px' }}>
                    {simResult.status === 200 && simResult.targetId === '102' && currentUser?.id === '101' && (
                      <div style={{ padding: '8px 12px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: '4px', fontSize: '12px', color: '#991b1b' }}>
                        <strong>Vulnerability Result:</strong> User A successfully retrieved User B's private record without authorization (IDOR vulnerability confirmed).
                      </div>
                    )}
                    {simResult.status === 403 && (
                      <div style={{ padding: '8px 12px', background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '4px', fontSize: '12px', color: '#166534' }}>
                        <strong>Remediation Verified:</strong> Request denied with 403 Forbidden. Server ownership check blocked cross-tenant access.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Postman Procedure Summary */}
              <div className="notice-box">
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
