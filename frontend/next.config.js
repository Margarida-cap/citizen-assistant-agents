/** next.config.js **/
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/agent/:path*',
        destination: 'http://localhost:8000/agent/:path*'
      }
    ];
  }
};

module.exports = nextConfig;
