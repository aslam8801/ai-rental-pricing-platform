import { useState } from "react";
import axios from "axios";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

export default function Dashboard() {

  const [formData, setFormData] = useState({
    sqft: "",
    bedrooms: "",
    school_score: "",
    noise: "",
  });

  const [predictedRent, setPredictedRent] = useState(null);

  const [comparables, setComparables] = useState([]);

  // =========================
  // Backend URL
  // =========================

  const API_BASE_URL =
    "https://ai-rental-pricing-platform.onrender.com";

  // =========================
  // Chart Data
  // =========================

  const chartData = [
    {
      name: "Area",
      value: Number(formData.sqft || 0),
    },
    {
      name: "Schools",
      value: Number(formData.school_score || 0),
    },
    {
      name: "Noise",
      value: Number(formData.noise || 0),
    },
  ];

  // =========================
  // Handle Input Change
  // =========================

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

  };

  // =========================
  // Predict Rent
  // =========================

  const predictRent = async () => {

    // Validation
    if (
      formData.sqft <= 0 ||
      formData.bedrooms <= 0 ||
      formData.school_score < 1 ||
      formData.school_score > 10 ||
      formData.noise < 1 ||
      formData.noise > 10
    ) {
      alert("Please enter valid property values");
      return;
    }

    try {

      // =========================
      // Predict Rent API
      // =========================

      const predictionResponse = await axios.post(
        `${API_BASE_URL}/predict`,
        {
          sqft: Number(formData.sqft),
          bedrooms: Number(formData.bedrooms),
          school_score: Number(formData.school_score),
          noise: Number(formData.noise),
        }
      );

      setPredictedRent(
        predictionResponse.data.predicted_rent
      );

      // =========================
      // Similar Properties API
      // =========================

      const comparablesResponse = await axios.post(
        `${API_BASE_URL}/similar-properties`,
        {
          sqft: Number(formData.sqft),
          bedrooms: Number(formData.bedrooms),
          school_score: Number(formData.school_score),
          noise: Number(formData.noise),
        }
      );

      setComparables(
        comparablesResponse.data.comparables
      );

    } catch (error) {

      console.error(error);

      alert("Prediction failed");
    }
  };

  return (

    <div className="min-h-screen bg-gray-100 p-8">

      {/* ========================= */}
      {/* Title */}
      {/* ========================= */}

      <h1 className="text-4xl font-bold mb-8 text-center">
        AI Rental Intelligence Platform
      </h1>

      {/* ========================= */}
      {/* Property Form */}
      {/* ========================= */}

      <div className="bg-white p-6 rounded-xl shadow-md max-w-4xl mx-auto">

        <h2 className="text-2xl font-bold mb-6">
          Property Details
        </h2>

        <div className="grid grid-cols-2 gap-4">

          <input
            type="number"
            name="sqft"
            placeholder="Sqft"
            className="border p-3 rounded"
            onChange={handleChange}
          />

          <input
            type="number"
            name="bedrooms"
            placeholder="Bedrooms"
            className="border p-3 rounded"
            onChange={handleChange}
          />

          <input
            type="number"
            name="school_score"
            placeholder="School Score"
            className="border p-3 rounded"
            onChange={handleChange}
          />

          <input
            type="number"
            name="noise"
            placeholder="Noise Level"
            className="border p-3 rounded"
            onChange={handleChange}
          />

        </div>

        <button
          onClick={predictRent}
          className="mt-6 bg-black text-white px-6 py-3 rounded-lg"
        >
          Predict Rent
        </button>

      </div>

      {/* ========================= */}
      {/* Prediction Card */}
      {/* ========================= */}

      {predictedRent && (

        <div className="bg-white p-6 rounded-xl shadow-md mt-8 max-w-4xl mx-auto">

          <h2 className="text-2xl font-bold">
            Predicted Rent
          </h2>

          <p className="text-5xl text-green-600 mt-4 font-bold">
            ₹ {predictedRent}
          </p>

        </div>

      )}

      {/* ========================= */}
      {/* Explanation Cards */}
      {/* ========================= */}

      <div className="grid grid-cols-3 gap-4 mt-8 max-w-4xl mx-auto">

        <div className="bg-blue-100 p-4 rounded-lg">

          <h3 className="font-bold text-lg">
            Good Schools
          </h3>

          <p className="mt-2">
            Higher school score increased pricing.
          </p>

        </div>

        <div className="bg-red-100 p-4 rounded-lg">

          <h3 className="font-bold text-lg">
            Noise Impact
          </h3>

          <p className="mt-2">
            Lower noise improved valuation.
          </p>

        </div>

        <div className="bg-green-100 p-4 rounded-lg">

          <h3 className="font-bold text-lg">
            Large Area
          </h3>

          <p className="mt-2">
            Higher sqft raised estimated rent.
          </p>

        </div>

      </div>

      {/* ========================= */}
      {/* Analytics Chart */}
      {/* ========================= */}

      <div className="bg-white p-6 rounded-xl shadow-md mt-8 max-w-4xl mx-auto">

        <h2 className="text-2xl font-bold mb-6">
          Property Analytics
        </h2>

        <ResponsiveContainer width="100%" height={300}>

          <BarChart data={chartData}>

            <XAxis dataKey="name" />

            <YAxis />

            <Tooltip />

            <Bar dataKey="value" />

          </BarChart>

        </ResponsiveContainer>

      </div>

      {/* ========================= */}
      {/* Comparable Properties */}
      {/* ========================= */}

      <div className="bg-white p-6 rounded-xl shadow-md mt-8 max-w-4xl mx-auto">

        <h2 className="text-2xl font-bold mb-6">
          Similar Properties
        </h2>

        <table className="w-full border">

          <thead>

            <tr className="bg-gray-100">

              <th className="p-3 border">
                Sqft
              </th>

              <th className="p-3 border">
                Bedrooms
              </th>

              <th className="p-3 border">
                School Score
              </th>

              <th className="p-3 border">
                Noise
              </th>

              <th className="p-3 border">
                Rent
              </th>

            </tr>

          </thead>

          <tbody>

            {comparables.map((property) => (

              <tr key={property.id}>

                <td className="p-3 border">
                  {property.sqft}
                </td>

                <td className="p-3 border">
                  {property.bedrooms}
                </td>

                <td className="p-3 border">
                  {property.school_score}
                </td>

                <td className="p-3 border">
                  {property.noise}
                </td>

                <td className="p-3 border">
                  ₹ {property.rent}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

      {/* ========================= */}
      {/* Map */}
      {/* ========================= */}

      <div className="bg-white p-6 rounded-xl shadow-md mt-8 max-w-4xl mx-auto">

        <h2 className="text-2xl font-bold mb-6">
          Property Location
        </h2>

        <MapContainer
          center={[19.0760, 72.8777]}
          zoom={12}
          style={{
            height: "400px",
            width: "100%",
          }}
        >

          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <Marker position={[19.0760, 72.8777]}>

            <Popup>
              Comparable Property
            </Popup>

          </Marker>

        </MapContainer>

      </div>

    </div>
  );
}