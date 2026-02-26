import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  /* config options here */
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
  serverExternalPackages: ['picocolors', 'postcss'],
  experimental: {
    turbo: {
      resolveExtensions: ['.js', '.jsx', '.ts', '.tsx', '.json'],
    },
  },
};

export default nextConfig;
