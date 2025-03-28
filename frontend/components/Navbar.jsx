import Link from 'next/link'

export default function Navbar() {
  return (
    <nav className="bg-primary text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link href="/" className="text-2xl font-bold">
            BrandEX
          </Link>
          <div className="flex space-x-6">
            <Link href="/influencer" className="hover:text-secondary transition">
              Influencer
            </Link>
            <Link href="/brand" className="hover:text-secondary transition">
              Brand
            </Link>
            <Link href="/admin" className="hover:text-secondary transition">
              Admin
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
