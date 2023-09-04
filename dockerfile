# Gunakan base image Python versi 3.11
FROM python:3.11

# Environment
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8192
ENV APP_ENV=dev
ENV DB_HOST=36.88.32.238
ENV DB_USER=postgres
ENV DB_PASS=k0pl4k
ENV DB_NAME=postgres
ENV DB_PORT=1032
ENV SECRET_KEY=w12e12e23e2we12e12e

# Buat direktori kerja dalam container
WORKDIR /app

# Salin file requirements.txt ke dalam direktori kerja
COPY requirements.txt .

# Instal dependensi yang dibutuhkan
RUN pip install -r requirements.txt

# Salin aplikasi Anda ke dalam direktori kerja
COPY . .

# Tentukan port yang akan digunakan oleh aplikasi Anda
EXPOSE 8192

# Perintah untuk menjalankan aplikasi Anda
CMD ["python", "app.py"]
