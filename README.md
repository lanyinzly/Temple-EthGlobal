# Temple

Rich Temple

1. 启动后端服务

# 进入后端目录

cd /Users/yushenli/Documents/my_code/Temple/backend

# 启动服务器

python start_server.py

后端服务将在 http://127.0.0.1:8000 运行

2. 启动前端服务

# 新开一个终端，进入前端目录

cd /Users/yushenli/Documents/my_code/Temple/frontend

# 安装依赖（如果还没有安装）

npm install

# 启动前端开发服务器

npm run dev

前端服务将在 http://localhost:3000 运行

3. 访问应用

打开浏览器访问：http://localhost:3000

4. 验证功能

1. 健康检查：访问 http://127.0.0.1:8000/api/health
1. API 文档：访问 http://127.0.0.1:8000/docs
1. 算卦流程：

   - 点击"算卦" → 输入问题 → 选择三个数字 → 查看 AI 生成的真实占卜结果

1. 测试后端（可选）

# 在后端目录运行测试客户端

cd /Users/yushenli/Documents/my_code/Temple/backend
python test_client.py

📝 注意事项

- 环境变量：确保 .env 文件中的 DEEPSEEK_API_KEY 已正确设置
- 端口占用：如果端口被占用，可以修改配置文件中的端口号
- 依赖安装：前端需要 Node.js 环境，后端需要 Python 3.10+

🔧 故障排除

如果遇到问题：

1. 后端无法启动：检查端口 8000 是否被占用
2. 前端无法连接后端：确认后端服务正在运行
3. 算卦功能异常：检查 DeepSeek API 密钥是否有效

现在你可以体验完整的 AI 算卦功能了！🔮
