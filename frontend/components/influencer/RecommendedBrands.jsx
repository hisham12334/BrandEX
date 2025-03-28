export default function RecommendedBrands() {
  const brands = [
    {
      id: 1,
      name: "UrbanVogue",
      industry: "Fashion",
      matchScore: 92,
      description: "Contemporary streetwear brand looking for influencers"
    },
    {
      id: 2, 
      name: "TechNova",
      industry: "Technology",
      matchScore: 87,
      description: "Gadget review opportunities for tech influencers"
    },
    {
      id: 3,
      name: "FreshBites",
      industry: "Food",
      matchScore: 85,
      description: "Healthy snack brand seeking food content creators"
    }
  ]

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Recommended Brands</h2>
      
      <div className="space-y-4">
        {brands.map(brand => (
          <div key={brand.id} className="border-b pb-4 last:border-b-0">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-medium">{brand.name}</h3>
                <p className="text-sm text-gray-600">{brand.industry}</p>
                <p className="text-sm mt-1">{brand.description}</p>
              </div>
              <div className="bg-primary text-white px-3 py-1 rounded-full text-sm">
                {brand.matchScore}% Match
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
