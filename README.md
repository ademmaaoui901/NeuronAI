# NeuronAI
**NeuronAI - نظام ذكاء اصطناعي متكامل يعمل كوكيل ذكي، قادر على إنشـاء أكواد متقدمة، توليد صور 4K، معالجة الصوت، إنشاء فيديوهات، وحل جميع المهام المعقدة.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![Celery](https://img.shields.io/badge/Celery-5.3.4-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Redis](https://img.shields.io/badge/Redis-7.2-red)
![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue)

---

## 🎯 **المقدمة**

هذا **نظام ذكاء اصطناعي متكامل** تم بناؤه خصيصاً لتلبية جميع متطلباتك:

✅ **وكيل ذكي** يعمل في الخلفية
✅ **أقوى نماذج مفتوحة المصدر** (CodeLlama, Mistral, SDXL, Whisper, XTTS)
✅ **إنشاء أكواد متقدمة** (20+ لغة برمجة)
✅ **توليد صور 4K** احترافية
✅ **معالجة الصوت** (صوت ←→ نص)
✅ **إنشاء فيديوهات** (قيد التطوير)
✅ **دعم العديد من المستخدمين** (Multi-user)
✅ **مهام خلفية** (Background Tasks)
✅ **واجهة API موحدة** (FastAPI)
✅ **سريع جداً** (GPU Acceleration)
✅ **يعمل محلياً** (On-premise)
✅ **مفتوح المصدر** (Open Source)

---

## 📁 **هيكل المشروع**

```
NeuronAI/
├── api/                          # FastAPI Application
│   ├── __init__.py
│   ├── main.py                   # Main application
│   ├── database/                 # Database configuration
│   │   ├── __init__.py
│   │   └── models/               # Database models
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── task.py
│   │       ├── conversation.py
│   │       └── project.py
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── chat.py
│   │   ├── code.py
│   │   ├── image.py
│   │   └── audio.py
│   └── endpoints/                # API endpoints
│       ├── __init__.py
│       ├── health.py
│       ├── users.py
│       ├── chat.py
│       ├── code.py
│       ├── image.py
│       ├── video.py
│       ├── audio.py
│       └── tasks.py
│
├── core/                         # Core AI Components
│   ├── __init__.py
│   ├── agent.py                  # Main AI Agent
│   └── security.py               # Security utilities
│
├── workers/                      # Celery Workers
│   ├── __init__.py
│   ├── celery_app.py             # Celery application
│   └── tasks/                    # Celery tasks
│       ├── __init__.py
│       ├── code_tasks.py
│       ├── image_tasks.py
│       ├── video_tasks.py
│       ├── audio_tasks.py
│       └── general_tasks.py
│
├── config/                       # Configuration
│   ├── __init__.py
│   ├── settings.py               # Application settings
│   └── model_config.py           # AI model configuration
│
├── docker/                       # Docker Configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env.example
│   └── nginx.conf
│
├── models/                       # AI Models (will be downloaded)
│   ├── llm/
│   ├── vision/
│   └── audio/
│
├── storage/                      # Storage
│   ├── uploads/
│   ├── outputs/
│   └── cache/
│
├── scripts/                      # Utility Scripts
├── tests/                        # Tests
├── .gitignore
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 **البدء السريع**

### **1️⃣ المتطلبات**

#### **متطلبات النظام:**
- **Python**: 3.10+
- **RAM**: 32GB+ (64GB+ للنماذج الكبيرة)
- **GPU**: NVIDIA CUDA (RTX 3090/4090 or A100)
- **VRAM**: 24GB+ (لCodeLlama-7B + SDXL)
- **Storage**: 200GB+ SSD
- **OS**: Ubuntu 22.04 LTS (recommended)

#### **متطلبات البرمجية:**
- Docker 20.10+
- Docker Compose 2.0+
- NVIDIA Container Toolkit (for GPU support)

### **2️⃣ التثبيت**

#### **طريقة 1: باستخدام Docker (موصى بها)**

```bash
# 1. انسخ المستودع
cd /workspace/NeuronAI

# 2. انسخ ملف البيئة
cp docker/.env.example docker/.env

# 3. عدل ملف .env (اختياري)
# - ضبط SECRET_KEY
# - ضبط DATABASE_URL
# - ضبط REDIS_URL
# - ضبط نماذج الذكاء الاصطناعي

# 4. أنشئ وابدأ الحاويات
cd docker
docker-compose up -d

# 5. انتظر حتى يتم تحميل جميع الحاويات
# (قد يستغرق عدة دقائق)
docker-compose logs -f
```

#### **طريقة 2: التثبيت اليدوي**

```bash
# 1. انسخ المستودع
cd /workspace/NeuronAI

# 2. أنشئ بيئة افتراضية
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. أنشئ قاعدة البيانات
# تأكد من تثبيت PostgreSQL
# ثم نفذ:
# createdb ai_agent
# psql ai_agent < schema.sql (إذا كان هناك)

# 5. أنشئ ملف .env
cp docker/.env.example .env
# عدل الملف حسب احتياجاتك

# 6. بدأ الخادم
uvicorn api.main:app --host 0.0.0.0 --port 8000

# 7. في نافذة أخرى، بدأ Celery
celery -A workers.celery_app worker --loglevel=info

# 8. بدأ Celery Beat (لمهام مجدولة)
celery -A workers.celery_app beat --loglevel=info

# 9. بدأ Flower (لمراقبة Celery)
celery -A workers.celery_app flower --port=5555
```

### **3️⃣ الوصول إلى النظام**

بعد التثبيت:
- **API**: `http://localhost:8000`
- **Docs (Swagger)**: `http://localhost:8000/docs`
- **Redoc**: `http://localhost:8000/redoc`
- **Flower (Celery Monitoring)**: `http://localhost:5555`

---

## 🌍 **ميزات النظام الكاملة**

### **📝 واجهة API**

| **النقطة النهائية** | **الغرض** | **الطريقة** | **المصادقة** |
|---------------------|------------|--------------|---------------|
| `/api/v1/users/register` | تسجيل مستخدم جديد | POST | ❌ |
| `/api/v1/users/login` | تسجيل الدخول | POST | ❌ |
| `/api/v1/users/me` | معلومات المستخدم | GET | ✅ |
| `/api/v1/users/` | قائمة المستخدمين | GET | ✅ (Admin) |
| `/api/v1/chat/` | محادثة مع الذكاء الاصطناعي | POST | ✅ |
| `/api/v1/code/generate` | توليد كود | POST | ✅ |
| `/api/v1/code/fix` | إصلاح كود | POST | ✅ |
| `/api/v1/code/explain` | شرح كود | POST | ✅ |
| `/api/v1/code/project` | إنشاء مشروع | POST | ✅ |
| `/api/v1/code/apk` | إنشاء APK | POST | ✅ |
| `/api/v1/image/generate` | توليد صورة | POST | ✅ |
| `/api/v1/image/edit` | تعديل صورة | POST | ✅ |
| `/api/v1/image/4k` | توليد صورة 4K | POST | ✅ |
| `/api/v1/audio/stt` | صوت إلى نص | POST | ✅ |
| `/api/v1/audio/tts` | نص إلى صوت | POST | ✅ |
| `/api/v1/video/generate` | توليد فيديو | POST | ✅ |
| `/api/v1/tasks/` | إنشاء مهمة | POST | ✅ |
| `/api/v1/tasks/` | قائمة المهام | GET | ✅ |
| `/api/v1/tasks/{id}` | معلومات المهمة | GET | ✅ |
| `/api/v1/tasks/{id}/status` | حالة المهمة | GET | ✅ |
| `/api/v1/health/` | فحص صحة النظام | GET | ❌ |

### **💻 إنشاء الأكواد**

**المميزات:**
- ✅ **توليد كود** من الوصف (20+ لغة)
- ✅ **إصلاح أخطاء** الكود تلقائياً
- ✅ **شرح الكود** بشكل مفصل
- ✅ **إنشاء مشاريع كاملة** (Web, Mobile, Desktop)
- ✅ **إنشاء تطبيقات اندرويد** (APK)
- ✅ **دعم جميع لغات البرمجة** الشهيرة

**النماذج المستخدمة:**
- **CodeLlama-7B** (أفضل نموذج مفتوح المصدر للأكواد)
- **Mistral-7B** (للفهم العام)

**أمثلة:**
```bash
# توليد كود Python
curl -X POST http://localhost:8000/api/v1/code/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": "Create a Python function to sort a list", "language": "python"}'

# إصلاح كود
curl -X POST http://localhost:8000/api/v1/code/fix \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b) return a + b", "language": "python"}'

# إنشاء مشروع كامل
curl -X POST http://localhost:8000/api/v1/code/project \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "my_project", "description": "A task management system", "language": "python"}'
```

### **🎨 توليد الصور**

**المميزات:**
- ✅ **توليد صور** من الوصف النصي
- ✅ **صور 4K** (2048x2048)
- ✅ **تعديل الصور** الموجودة
- ✅ **دعم جميع الأنماط الفنية**

**النماذج المستخدمة:**
- **Stable Diffusion XL** (أفضل نموذج مفتوح المصدر للصور)

**أمثلة:**
```bash
# توليد صورة
curl -X POST http://localhost:8000/api/v1/image/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A beautiful sunset over mountains, digital art", "width": 1024, "height": 1024}'

# توليد صورة 4K
curl -X POST http://localhost:8000/api/v1/image/4k \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A futuristic city at night, cyberpunk style"}'
```

### **🎤 معالجة الصوت**

**المميزات:**
- ✅ **صوت إلى نص** (99+ لغة)
- ✅ **نص إلى صوت** (50+ لغة)
- ✅ **دعم اللهجات العربية**
- ✅ **جودة عالية**

**النماذج المستخدمة:**
- **Whisper-Large** (أفضل نموذج مفتوح المصدر للصوت إلى نص)
- **XTTS v2** (أفضل نموذج مفتوح المصدر للنص إلى صوت)

**أمثلة:**
```bash
# تحويل صوت إلى نص
curl -X POST http://localhost:8000/api/v1/audio/stt/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "audio_file=@audio.wav" \
  -F "language=ar"

# تحويل نص إلى صوت
curl -X POST http://localhost:8000/api/v1/audio/tts \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "مرحبا بالعالم", "language": "ar"}'
```

### **🎬 توليد الفيديوهات**

**المميزات:**
- ⚠️ **قيد التطوير** (يحتاج إلى Stable Video Diffusion)
- ✅ **إنشاء فيديوهات** من صور
- ✅ **تحويل الصور إلى فيديو**

**المتطلبات:**
- GPU: 24GB+ VRAM
- Model: Stable Video Diffusion

### **🤖 الوكيل الذكي**

**المميزات:**
- ✅ **تفكير منطقي** (Chain-of-Thought)
- ✅ **حل المشكلات** المعقدة
- ✅ **اتخاذ القرارات** الذكية
- ✅ **تنفيذ مهام متعددة** في الخلفية

**أمثلة:**
```bash
# محادثة مع الذكاء الاصطناعي
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "كيف أبدأ مشروعاً جديداً؟"}]}'
```

---

## 📊 **نماذج الذكاء الاصطناعي المستخدمة**

| **النوع** | **النموذج** | **الحجم** | **الدقة** | **GPU مطلوب** | **الاستخدام** |
|-----------|-------------|-----------|-----------|----------------|---------------|
| **LLM (كتابة أكواد)** | CodeLlama-7B | 14GB | ⭐⭐⭐⭐⭐ | 24GB VRAM | توليد وإصلاح الكود |
| **LLM (فهم عام)** | Mistral-7B | 14GB | ⭐⭐⭐⭐⭐ | 24GB VRAM | المحادثة والفهم |
| **Vision (صور)** | Stable Diffusion XL | 6GB | ⭐⭐⭐⭐⭐ | 16GB VRAM | توليد الصور |
| **Audio (STT)** | Whisper-Large | 3GB | ⭐⭐⭐⭐⭐ | 8GB VRAM | صوت إلى نص |
| **Audio (TTS)** | XTTS v2 | 1.5GB | ⭐⭐⭐⭐ | 8GB VRAM | نص إلى صوت |
| **Video** | Stable Video Diffusion | 10GB | ⭐⭐⭐⭐ | 24GB VRAM | توليد الفيديوهات |

**الإجمالي:** ~48GB (جميع النماذج)

---

## ⚡ **الأداء**

### **متطلبات الخادم**

| **المكون** | **المتطلب** | **ملاحظة** |
|------------|--------------|-------------|
| **GPU** | NVIDIA A100 (80GB) | أفضل أداء |
| **GPU** | 2x RTX 4090 (48GB) | بديل جيد |
| **VRAM** | 80GB+ | لCodeLlama-7B + SDXL |
| **RAM** | 128GB+ | دعم العديد من المستخدمين |
| **CPU** | 32+ Core | لتشغيل Celery |
| **Storage** | 1TB+ NVMe SSD | للنماذج والملفات |
| **OS** | Ubuntu 22.04 LTS | أفضل دعم |

### **الأداء المتوقع**

| **المهمة** | **الوقت (GPU)** | **الوقت (CPU)** | **RAM مطلوب** |
|------------|-----------------|-----------------|----------------|
| توليد نص (512 token) | <1 ث | 2-5 ث | 4GB |
| توليد صورة (1024x1024) | 5-10 ث | 30-60 ث | 8GB |
| صوت ← نص (1 دقيقة) | 2-5 ث | 10-20 ث | 4GB |
| نص → صوت (10 ثوان) | 3-5 ث | 15-30 ث | 6GB |
| توليد فيديو (5 ثوان) | 10-20 ث | 60+ ث | 16GB |

---

## 🔧 **الإعدادات والتخصيص**

### **1. تغيير نماذج الذكاء الاصطناعي**

يمكنك تغيير النماذج في ملف `config/model_config.py`:

```python
# لاستخدام نماذج أكبر
CODE_LLAMA: Dict[str, Any] = field(default_factory=lambda: {
    "model_name": "codellama/CodeLlama-13b-Instruct-hf",  # 13B instead of 7B
    ...
})

MISTRAL: Dict[str, Any] = field(default_factory=lambda: {
    "model_name": "mistralai/Mistral-13B-Instruct-v0.1",  # 13B instead of 7B
    ...
})

# لاستخدام Stable Diffusion 1.5 بدلاً من XL
SDXL: Dict[str, Any] = field(default_factory=lambda: {
    "model_name": "runwayml/stable-diffusion-v1-5",
    ...
})
```

### **2. تغيير إعدادات الأداء**

في ملف `config/model_config.py`:

```python
# استخدام 8-bit بدلاً من 4-bit
USE_4BIT = False
USE_8BIT = True

# عدم استخدام GPU
USE_GPU = False

# عدم تحميل النماذج تلقائياً
OFFLOAD_TO_CPU = False
```

### **3. إضافة نماذج جديدة**

لإضافة نموذج جديد:

1. أضف الإعدادات في `config/model_config.py`
2. أضف دالة التحميل في `core/agent.py`
3. أضف الأدوات اللازمة في `core/agent.py`

### **4. تغيير إعدادات قاعدة البيانات**

في ملف `.env`:

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# SQLite (للاختبار)
DATABASE_URL=sqlite+aiosqlite:///./ai_agent.db
```

---

## 🌐 **نشر النظام**

### **1. نشر على خادم**

#### **متطلبات:**
- خادم مع GPU (A100 or RTX 4090)
- 128GB+ RAM
- 1TB+ SSD
- Ubuntu 22.04 LTS

#### **الخطوات:**

```bash
# 1. انسخ المستودع
cd /opt
sudo git clone https://github.com/your-username/NeuronAI.git
cd NeuronAI

# 2. انسخ ملف البيئة
sudo cp docker/.env.example docker/.env
sudo nano docker/.env  # عدل الإعدادات

# 3. أنشئ وابدأ الحاويات
sudo docker-compose -f docker/docker-compose.yml up -d

# 4. تأكد من أن جميع الحاويات تعمل
sudo docker-compose ps

# 5. تأكد من أن النماذج قد تم تحميلها
sudo docker-compose logs -f api
```

### **2. نشر على Hugging Face Spaces**

1. إنشاء حساب على [Hugging Face](https://huggingface.co)
2. إنشاء Space جديد
3. رفع الملفات
4. تحديد `api/main.py` كملف رئيسية
5. إضافة `requirements.txt`

**ملاحظة:** Hugging Face Spaces لا يدعم GPU قوياً كفاية للنماذج الكبيرة.

### **3. نشر على Google Cloud / AWS / Azure**

- **Google Cloud:** استخدم Compute Engine مع GPU
- **AWS:** استخدم EC2 (p4d.24xlarge or p3.8xlarge)
- **Azure:** استخدم Virtual Machines مع GPU

---

## 📚 **الأمثلة العملية**

### **مثال 1: إنشاء تطبيق ويب كامل**

```python
import requests
import json

# تسجيل الدخول
login_url = "http://localhost:8000/api/v1/users/login"
login_data = {
    "username": "your_username",
    "password": "your_password"
}
response = requests.post(login_url, json=login_data)
token = response.json()["access_token"]

# إنشاء مشروع
project_url = "http://localhost:8000/api/v1/code/project"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
project_data = {
    "name": "my_web_app",
    "description": "A blog website with user authentication",
    "language": "python"
}
response = requests.post(project_url, headers=headers, json=project_data)
print(response.json())
```

### **مثال 2: توليد صورة 4K**

```python
import requests
import json

# تسجيل الدخول (كما في المثال السابق)
# ...

# توليد صورة 4K
image_url = "http://localhost:8000/api/v1/image/4k"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "prompt": "A beautiful sunset over the ocean, ultra-realistic, 4K",
    "negative_prompt": "blurry, low quality, distorted"
}
response = requests.post(image_url, headers=headers, json=data)
print(response.json())
```

### **مثال 3: تحويل صوت إلى نص**

```python
import requests

# تسجيل الدخول (كما في المثال السابق)
# ...

# تحويل صوت إلى نص
stt_url = "http://localhost:8000/api/v1/audio/stt/upload"
headers = {
    "Authorization": f"Bearer {token}"
}
files = {
    "audio_file": open("audio.wav", "rb")
}
data = {
    "language": "ar"
}
response = requests.post(stt_url, headers=headers, files=files, data=data)
print(response.json())
```

---

## 🛠️ **استكشاف الأخطاء**

### **❌ مشكلة: "CUDA out of memory"**

**✅ الحلول:**
1. استخدم نماذج أصغر:
   ```python
   # في config/model_config.py
   CODE_LLAMA["model_name"] = "codellama/CodeLlama-7b-Instruct-hf"  # بدلاً من 13B
   ```
2. استخدام 4-bit quantization:
   ```python
   USE_4BIT = True
   ```
3. زيادة VRAM أو استخدام GPU أكبر
4. تقليل `max_tokens` في الطلبات

### **❌ مشكلة: "Model not found"**

**✅ الحلول:**
1. تأكد من اتصال الإنترنت
2. انتظر حتى يتم تحميل النموذج تلقائياً
3. تحميل النموذج يدوياً:
   ```bash
   cd models/llm
   wget https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf/resolve/main/*.gguf
   ```

### **❌ مشكلة: "Out of Memory" (RAM)**

**✅ الحلول:**
1. أغلق التاب غير المستخدمة
2. استخدم نماذج أصغر
3. زيادة RAM إلى 64GB+
4. استخدام offloading إلى CPU:
   ```python
   OFFLOAD_TO_CPU = True
   ```

### **❌ مشكلة: "Connection refused" (Redis/PostgreSQL)**

**✅ الحلول:**
1. تأكد من أن Docker يعمل
2. تأكد من أن الحاويات تعمل:
   ```bash
   docker ps
   ```
3. تأكد من أن المنافذ مفتوحة:
   ```bash
   netstat -tuln | grep 6379  # Redis
   netstat -tuln | grep 5432  # PostgreSQL
   ```

### **❌ مشكلة: "ModuleNotFoundError"**

**✅ الحلول:**
1. تثبيت المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```
2. تأكد من أن بيئة Python الصحيحة نشطة

---

## 💡 **النصائح**

### **للأداء:**
- ✅ استخدم GPU إذا كان متاحاً
- ✅ أغلق التاب غير المستخدمة لتحرير الذاكرة
- ✅ حدد نماذج أصغر إذا كانت الأجهزة محدودة
- ✅ استخدم 4-bit quantization لتوفير الذاكرة
- ✅ استخدم offloading إلى CPU إذا كانت VRAM محدودة

### **للأمان:**
- ✅ غير SECRET_KEY في ملف .env
- ✅ غير كلمات مرور قاعدة البيانات
- ✅ استخدم HTTPS في الإنتاج
- ✅ حدد CORS_ORIGINS بشكل صحيح
- ✅ لا تشارك API keys

### **للتطوير:**
- ✅ جرب نماذج مختلفة
- ✅ قرأ وثائق Hugging Face
- ✅ شارك مشروعاتك
- ✅ ساهم في المشروع

---

## 🤝 **الدعم**

إذا واجهت أي مشكلة أو تريد:
- ✅ **نماذج أكبر** (CodeLlama-13B, Mistral-13B)
- ✅ **دمج مع APIs حقيقية** (Booking.com, etc.)
- ✅ **واجهة مستخدم مخصصة** (Frontend)
- ✅ **نشر على السحابة**
- ✅ **إضافة ميزات جديدة**

**اتصل بي وسأساعدك!** 🚀

---

## 📄 **الترخيص**

هذا المشروع **مفتوح المصدر** تحت رخصة **MIT License**.

---

## 🎉 **الخلاصة**

لديك الآن **نظام ذكاء اصطناعي متكامل احترافي** يعمل كوكيل ذكي، قادر على:

✅ **إنشاء أكواد متقدمة** (20+ لغة)
✅ **توليد صور 4K** احترافية
✅ **معالجة الصوت** (صوت ←→ نص)
✅ **إنشاء فيديوهات** (قيد التطوير)
✅ **دعم العديد من المستخدمين**
✅ **مهام خلفية** (Background Tasks)
✅ **واجهة API موحدة**
✅ **سريع جداً** (GPU Acceleration)
✅ **يعمل محلياً** (On-premise)
✅ **مفتوح المصدر** (Open Source)

**ابدأ الاستخدام الآن!** 🚀

---

**تم تطوير هذا النظام خصيصاً لك من قبل Vibe Code** 🤖

*Version: 1.0.0*
*Last Updated: 2024*
*License: MIT*
