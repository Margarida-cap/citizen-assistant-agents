import React, { useEffect } from 'react';

const CLIENT_ID = "299771489297-hv6h409jk0se5ubn5bdmnajmnffibhdi.apps.googleusercontent.com";

const Login = ({ onLogin }) => {
  useEffect(() => {
    /* global google */
    if (window.google) {
      window.google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: handleCredentialResponse,
      });
      window.google.accounts.id.renderButton(
        document.getElementById("g_id_signin"),
        { theme: "outline", size: "large" }
      );
    }
  }, []);

  const handleCredentialResponse = (response) => {
    // response.credential is the JWT ID token
    onLogin(response.credential);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '3rem' }}>
      <div id="g_id_signin"></div>
    </div>
  );
};

export default Login;