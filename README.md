# 🔐 Secure File Sharing System – Django Backend

A secure file-sharing backend system built using Django and SQLite, with support for:

- Two user roles: **Ops** (admin uploaders) and **Clients** (verified downloaders)
- JWT-based authentication and email verification
- Secure file uploads and token-based downloads
- Complete API coverage with Postman Collection

## 📁 Project Structure

```
SECURE_FILE_SHARE/
├── backend/
│ ├── files/ # File upload/download logic
│ ├── media/uploads/ # Stored uploaded files
│ ├── secure_file_share/ # Django settings and WSGI
│ ├── uploads/ # File metadata or storage logic
│ └── users/ # User models and auth (Ops & Clients)
│
├── .gitignore
├── db.sqlite3 # SQLite database
├── manage.py # Django entry point
├── requirements.txt # Python dependencies
├── postman/ # Postman collection + env
```
## 🚀 Getting Started (Clone and Run)

### 1. Clone the repository
git clone [https://github.com//secure-share.git](https://github.com/excuation/secure_file_share.git)

cd backend
then python manage.py runserver


### 2. Create virtual environment
python -m venv venv
#### On Windows:   venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run migrations
for accessing the django admin panel  username is "admin" and password is "admin"

python manage.py migrate

### 5. Start the server
python manage.py runserver

## 🔐 Authentication & User Flow

---

### ✅ 1. Client Signup  
**POST** `/api/client/signup/`  
➡ Creates a new client user  
📸 Screenshot: ![Signup OK](https://raw.githubusercontent.com/excuation/secure_file_share/refs/heads/master/Postman%20Images/client-signup.png)

---

### 📧 2. Email Verification  
**GET** `/api/client/verify/?token=<verification_token>`  
➡ Activates the client account  
📸 Screenshot: ![Email Verified](https://github.com/CSEExplorer/secure_file_share/blob/master/Postman%20Images/verify-email.png)

---

### 🔐 3. Client Login  
**POST** `/api/client/login/`  
➡ Returns JWT token for authentication  
📸 Screenshot: ![Login OK](https://github.com/excuation/secure_file_share/blob/master/Postman%20Images/client-login.png)

---

### 🗂️ 4. Upload File (Ops only)  
**POST** `/api/files/upload/`  
➡ Auth: Ops JWT required  
📸 Screenshot: ![Upload OK](https://raw.githubusercontent.com/CSEExplorer/secure_file_share/refs/heads/master/Postman%20Images/file-upload.png)

---

### 📥 5. List Uploaded Files (Client only)  
**GET** `/api/files/list/`  
➡ Lists file names and metadata  
📸 Screenshot: ![File List](https://github.com/CSEExplorer/secure_file_share/blob/master/Postman%20Images/list-file.png)

---

### 🔓 6. Generate Download Link  
**POST** `/api/files/generate-download-link/{{file_id}}/`  
➡ Auth: Client JWT required  
➡ Body: `{ "filename": "xyz.pdf" }`  
📸 Screenshot: ![Download Token](https://raw.githubusercontent.com/CSEExplorer/secure_file_share/refs/heads/master/Postman%20Images/generate-download-link.png)

---

### 📥 7. Download File  
**GET** `/api/file/download/?token=<download_token>`  
➡ Secure one-time file access  
📸 Screenshot: ![Download OK](https://raw.githubusercontent.com/CSEExplorer/secure_file_share/refs/heads/master/Postman%20Images/download-file.png)

## 📦 Postman Collection

You can import the complete Postman Collection from this link:

🔗 [Secure File Sharing API Collection (JSON)](https://github.com/excuation/secure_file_share/blob/master/postman/Secure%20File%20Sharing%20API%20Collection.postman_collection.json)

---

### ✅ What This Collection Supports

- 🔐 **Token Extraction & Reuse**  
  Automatically captures and uses JWT tokens, email verification tokens, and download tokens across requests.

- ⚙️ **Pre-request Scripts**  
  Built-in scripts that set headers, environment variables, and prepare tokens before each request.

- 🔗 **Chained Requests**  
  Designed for full flow testing: Signup → Verify → Login → Upload → Download.

---

📁 The collection is located at:  
`/postman/Secure File Sharing API Collection.postman_collection.json`





## 📊 API Endpoint Summary

| **Endpoint**                              | **Method** | **Role** | **Auth Required** | **Description**                 |
|-------------------------------------------|------------|----------|-------------------|---------------------------------|
| `/api/client/signup/`                     | POST       | Client   | ❌                | Register a new client           |
| `/api/client/verify/`                     | GET        | Client   | ❌                | Verify email via token          |
| `/api/client/login/`                      | POST       | Client   | ❌                | Login and receive JWT           |
| `/api/file/upload/`                       | POST       | Ops      | ✅ (JWT)          | Upload file                     |
| `/api/file/list/`                         | GET        | Client   | ✅ (JWT)          | List uploaded files             |
| `/api/file/generate-load /`               | POST       | Client   | ✅ (JWT)          | Generate one-time token         |
| `/api/file/download/?token=xyz`           | GET        | Client   | ❌                | Download file using token       |

## 💡 Notes

- 🔐 **JWT tokens** are passed in headers like this:  
  `Authorization: Bearer <your_token_here>`

- 📧 **Email verification links** are simulated for testing purposes — tokens are printed in the console or logs. Use them manually in the browser or API call.

- 📥 **Download tokens** are **one-time use** and **expire immediately** after the file is downloaded. If expired or reused, the file will not be accessible.

- ✅ The system handles proper status codes and error responses for invalid or missing tokens.
