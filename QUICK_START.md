# 🚀 QUICK START GUIDE

## ✅ Backend is Already Running!

Your backend server is currently running on **http://localhost:8000**

---

## 🎯 Start the Frontend

Open a **NEW terminal** and run:

```bash
cd frontend
npm run dev
```

The frontend will start on **http://localhost:5173**

---

## 🧪 Test the Application

### 1. Open Browser
Navigate to: **http://localhost:5173**

### 2. Login
Use any of these test accounts:
- Username: `Imayavarman` / Password: `Imayavarman@2000`
- Username: `Kumar` / Password: `Kumar@2000`
- Username: `Senthilkumaran` / Password: `Senthilkumaran@2000`

**Note:** Username is the person's NAME, not the number!

### 3. Explore Dashboard
- View financial metrics
- Check expense breakdown
- See investment portfolio
- Try AI chat feature

---

## 🔍 Verify Everything Works

### Backend Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AUREXIS AI Backend",
  "version": "2.0"
}
```

### Frontend Check
- Open http://localhost:5173
- Should see login page
- No console errors in browser DevTools (F12)

---

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Then restart backend
cd backend
python server.py
```

**Module not found:**
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Kill the process and restart
npm run dev
```

**Dependencies missing:**
```bash
cd frontend
npm install
npm run dev
```

**Build errors:**
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📊 What's Working

✅ Backend API (60+ endpoints)  
✅ User authentication  
✅ Financial analytics  
✅ ML forecasting  
✅ Budget optimization  
✅ Tax planning  
✅ Fraud detection  
✅ Real-time alerts  
✅ Multi-agent system  
✅ Chat with AI (requires Ollama)  

---

## 🎨 Features to Test

### Dashboard
- Overview with key metrics
- Financial health score
- Expense breakdown
- Investment portfolio
- Goals tracking

### Analytics
- Monthly forecasts
- Net worth projections
- Expense trends
- Savings projections

### AI Features
- Budget optimization
- Credit score prediction
- Tax planning
- Fraud detection
- Smart recommendations

### Chat
- AI financial advisor
- Personalized advice
- Multi-agent workflows

---

## 🔧 Optional: Enable AI Chat

If you want the AI chat feature to work:

### 1. Install Ollama
Download from: https://ollama.ai

### 2. Start Ollama
```bash
ollama serve
```

### 3. Pull the Model
```bash
ollama pull deepseek-v3.1:671b-cloud
```

### 4. Test Chat
- Go to dashboard
- Click chat icon
- Ask: "What's my financial health?"

---

## 📝 Development Workflow

### Making Changes

**Backend changes:**
- Edit files in `backend/`
- Server auto-reloads (uvicorn --reload)
- Check terminal for errors

**Frontend changes:**
- Edit files in `frontend/src/`
- Vite auto-reloads
- Check browser console for errors

### Testing

**Backend:**
```bash
cd backend
pytest tests/
```

**Frontend:**
```bash
cd frontend
npm test
```

---

## 🎯 Next Steps

1. ✅ Backend running
2. ⏳ Start frontend
3. ⏳ Test login with: **Imayavarman** / **Imayavarman@2000**
4. ⏳ Explore features
5. ⏳ Try AI chat (optional)

---

## 📚 Documentation

- `MIGRATION.md` - Breaking changes guide
- `ALL_BUGS_FIXED.md` - Complete bug fix report
- `API_DOCUMENTATION.md` - API endpoints reference
- `README.md` - Project overview

---

## 💡 Tips

- Keep backend terminal open to see logs
- Use browser DevTools (F12) to debug frontend
- Check `backend/logs/aurexis.log` for detailed logs
- Use `/health` endpoint to verify backend status

---

**Happy Coding! 🚀**

*Your AUREXIS AI application is ready to use!*
