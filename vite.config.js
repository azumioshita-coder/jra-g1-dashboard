import { defineConfig } from 'vite';

export default defineConfig({
  base: './', // アセットの読み込みパスを相対パスにし、ローカルファイル（file:///）や様々なURL階層でも正常にロード可能にする
  server: {
    host: true, // すべてのネットワークインターフェースからのアクセスを許可
    allowedHosts: true, // プロキシ経由等のすべてのホストヘッダーを許可
    cors: true, // CORSを許可
  }
});
