# 🔍 Simple Network Scanner – Web App

A web-based network scanner built with **Flask** and **PostgreSQL**, allowing registered users to scan local IP ranges for open ports.

> ❗ This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.  
> **Commercial use is strictly prohibited.**

---

## ✨ Features

- 🌐 Scan a local IP subnet (e.g., `192.168.1.0/24`)
- 🔐 User registration & login system
- 🛠️ Open port detection using Python sockets (no external tools like `nmap`)
- 📜 Scan history per user (stored in PostgreSQL)
- ☁️ Deployable on **Render’s free tier**

---

## 🚀 Getting Started (Local Dev)

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/network-scanner.git
cd network-scanner
