# YZAK Store

A full-stack fashion e-commerce platform built with modern web technologies.

## Features

- Product listings with categories and filtering
- Shopping cart and checkout flow
- User authentication and order management
- Responsive design across all devices
- Clean, minimal UI focused on the shopping experience

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Backend | Node.js, Express |
| Database | MongoDB |
| Deployment | Vercel |

## Getting Started

```bash
git clone https://github.com/isakhu/yzak-store
cd yzak-store
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

Create a `.env.local` file:

```env
MONGODB_URI=your_mongodb_connection_string
NEXTAUTH_SECRET=your_secret
NEXTAUTH_URL=http://localhost:3000
```

## Project Structure

```
├── app/
│   ├── (auth)/
│   ├── products/
│   ├── cart/
│   └── checkout/
├── components/
├── lib/
└── public/
```

## Author

**Yishak Tule** — [yishak-tule.vercel.app](https://yishak-tule.vercel.app)
