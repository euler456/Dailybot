FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装 GTK+ 依赖
RUN apt update && apt install -y \
    libgtk-3-dev \
    libglib2.0-dev \
    libgdk-pixbuf2.0-dev \
    libpango1.0-dev \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    build-essential \
    libjpeg-dev \
    libtiff-dev \
    libpng-dev

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行主程序
CMD ["python", "main.py"]
