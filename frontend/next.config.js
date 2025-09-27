/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
  env: {
    PORT: '3001',
  },
  // Suppress hydration warnings for browser extension attributes
  experimental: {
    suppressHydrationWarning: true,
  },
  // Custom webpack configuration to handle browser extension attributes
  webpack: (config, { isServer }) => {
    if (!isServer) {
      // Suppress hydration warnings for specific attributes
      config.resolve.fallback = {
        ...config.resolve.fallback,
      };
    }
    return config;
  },
};

module.exports = nextConfig;
