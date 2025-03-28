import Head from 'next/head'
import Navbar from './Navbar'

export default function Layout({ children }) {
  return (
    <>
      <Head>
        <title>BrandEX Platform</title>
        <meta name="description" content="Brand-Influencer Matching Platform" />
      </Head>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-grow container mx-auto px-4 py-8">
          {children}
        </main>
        <footer className="bg-dark text-white py-4">
          <div className="container mx-auto px-4 text-center">
            © {new Date().getFullYear()} BrandEX Platform
          </div>
        </footer>
      </div>
    </>
  )
}
