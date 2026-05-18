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

export default function Dashboard() {

  const [formData, setFormData] = useState({

    locality: "",

    sqft: "",

    bedrooms: "",

    metro_distance_km: "",

    hospital_distance_km: "",

    flood_risk: ""

  });

  const [predictedRent, setPredictedRent] =
    useState(null);

  const [comparables, setComparables] =
    useState([]);

  const [explanations, setExplanations] =
    useState([]);

  // =========================
  // BACKEND URL
  // =========================

  const API_BASE_URL =
    "https://ai-rental-pricing-platform.onrender.com";

  

  // =========================
  // HANDLE INPUT
  // =========================

  const handleChange = (e) => {

    setFormData({

      ...formData,

      [e.target.name]: e.target.value,
    });
  };

  // =========================
  // CHART DATA
  // =========================

  const chartData = [

    {
      name: "Sqft",
      value: Number(formData.sqft || 0),
    },

    {
      name: "Bedrooms",
      value: Number(formData.bedrooms || 0),
    },

    {
      name: "Metro",
      value: Number(
        formData.metro_distance_km || 0
      ),
    },

    {
      name: "Flood Risk",
      value: Number(
        formData.flood_risk || 0
      ),
    },
  ];

  // =========================
  // PREDICT RENT
  // =========================

  const predictRent = async () => {

    try {

      const response = await axios.post(

        `${API_BASE_URL}/predict`,

        {

          locality: formData.locality,

          sqft: Number(formData.sqft),

          bedrooms: Number(formData.bedrooms),

          metro_distance_km: Number(
            formData.metro_distance_km
          ),

          hospital_distance_km: Number(
            formData.hospital_distance_km
          ),

          flood_risk: Number(
            formData.flood_risk
          )
        }
      );

      setPredictedRent(
        response.data.predicted_rent
      );

      setComparables(
        response.data.comparables
      );

      setExplanations(
        response.data.explanation
      );

    } catch (error) {

      console.error(error);

      alert("Prediction failed");
    }
  };

  return (

    <div className="min-h-screen bg-gray-100 p-8">

      {/* ========================= */}
      {/* TITLE */}
      {/* ========================= */}

      <h1 className="text-5xl font-bold mb-10 text-center">

        AI Rental Intelligence Platform

      </h1>

      {/* ========================= */}
      {/* PROPERTY FORM */}
      {/* ========================= */}

      <div className="bg-white p-8 rounded-2xl shadow-md max-w-5xl mx-auto">

        <h2 className="text-3xl font-bold mb-8">

          Property Details

        </h2>

        <div className="grid grid-cols-2 gap-5">

          <input
            type="text"
            name="locality"
            placeholder="Locality / Area"
            className="border p-4 rounded-lg"
            onChange={handleChange}
          />

          <input
            type="number"
            name="sqft"
            placeholder="Area (Sqft)"
            className="border p-4 rounded-lg"
            onChange={handleChange}
          />

          <input
            type="number"
            name="bedrooms"
            placeholder="BHK"
            className="border p-4 rounded-lg"
            onChange={handleChange}
          />

          <input
            type="number"
            name="metro_distance_km"
            placeholder="Metro Distance (KM)"
            className="border p-4 rounded-lg"
            onChange={handleChange}
          />

          <input
            type="number"
            name="hospital_distance_km"
            placeholder="Hospital Distance (KM)"
            className="border p-4 rounded-lg"
            onChange={handleChange}
          />

          <input
            type="number"
            name="flood_risk"
            placeholder="Flood Risk (1-10)"
            className="border p-4 rounded-lg"
            onChange={handleChange}
          />

        </div>

        <button
          onClick={predictRent}
          className="mt-8 bg-black text-white px-8 py-4 rounded-xl"
        >

          Predict Rent

        </button>

      </div>

      {/* ========================= */}
      {/* RENT OUTPUT */}
      {/* ========================= */}

      {

        predictedRent && (

          <div className="bg-white p-8 rounded-2xl shadow-md mt-10 max-w-5xl mx-auto">

            <h2 className="text-3xl font-bold">

              Estimated Market Rent

            </h2>

            <p className="text-6xl text-green-600 mt-6 font-bold">

              ₹ {predictedRent}

            </p>

          </div>
        )
      }

      {/* ========================= */}
      {/* EXPLANATIONS */}
      {/* ========================= */}

      {

        explanations.length > 0 && (

          <div className="grid grid-cols-3 gap-5 mt-10 max-w-5xl mx-auto">

            {

              explanations.map(

                (item, index) => (

                  <div
                    key={index}
                    className="bg-blue-100 p-5 rounded-xl"
                  >

                    <h3 className="font-bold text-xl">

                      Pricing Insight

                    </h3>

                    <p className="mt-3">

                      {item}

                    </p>

                  </div>
                )
              )
            }

          </div>
        )
      }

      {/* ========================= */}
      {/* ANALYTICS */}
      {/* ========================= */}

      <div className="bg-white p-8 rounded-2xl shadow-md mt-10 max-w-5xl mx-auto">

        <h2 className="text-3xl font-bold mb-8">

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
      {/* COMPARABLE PROPERTIES */}
      {/* ========================= */}

      <div className="bg-white p-8 rounded-2xl shadow-md mt-10 max-w-6xl mx-auto">

        <h2 className="text-3xl font-bold mb-8">

          Comparable Properties

        </h2>

        <table className="w-full border">

          <thead>

            <tr className="bg-gray-100">

              <th className="p-4 border">
                Locality
              </th>

              <th className="p-4 border">
                Rent
              </th>

              <th className="p-4 border">
                Sqft
              </th>

              <th className="p-4 border">
                Bedrooms
              </th>

              <th className="p-4 border">
                Metro Distance
              </th>

              <th className="p-4 border">
                Similarity
              </th>

            </tr>

          </thead>

          <tbody>

            {

              comparables.map((property) => (

                <tr key={property.id}>

                  <td className="p-4 border">
                    {property.locality}
                  </td>

                  <td className="p-4 border">
                    ₹ {property.rent}
                  </td>

                  <td className="p-4 border">
                    {property.sqft}
                  </td>

                  <td className="p-4 border">
                    {property.bedrooms}
                  </td>

                  <td className="p-4 border">
                    {
                      property.metro_distance_km
                    } km
                  </td>

                  <td className="p-4 border">
                    {
                      property.similarity_score
                    }
                  </td>

                </tr>
              ))
            }

          </tbody>

        </table>

      </div>

    </div>
  );
}