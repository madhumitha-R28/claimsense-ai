import { useState } from "react";
import axios from "axios";
import "./App.css";
const API_URL = "http://127.0.0.1:8000";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [claims, setClaims] = useState([]);

  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    policy_number: "",
    claim_amount: "",
    hospital_name: "",
    diagnosis: ""
  });

  const [loading, setLoading] = useState(false);

  // ============================================================
  // LOGIN
  // ============================================================

  const handleLogin = async (event) => {
    event.preventDefault();

    setMessage("");
    setLoading(true);

    try {
      const form = new URLSearchParams();

      form.append("username", username);
      form.append("password", password);

      const response = await axios.post(
        `${API_URL}/login`,
        form,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          }
        }
      );

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      setIsLoggedIn(true);

      setMessage("Login successful!");

      setUsername("");
      setPassword("");

    } catch (error) {
      console.error(error);

      if (error.response) {
        setMessage(
          error.response.data.detail ||
          "Login failed"
        );
      } else {
        setMessage(
          "Unable to connect to the server"
        );
      }

    } finally {
      setLoading(false);
    }
  };


  // ============================================================
  // GET CLAIMS
  // ============================================================

  const fetchClaims = async () => {
    try {
      const token =
        localStorage.getItem("access_token");

      const response = await axios.get(
        `${API_URL}/claims`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setClaims(response.data.claims);

    } catch (error) {
      console.error(error);

      if (error.response?.status === 401) {
        localStorage.removeItem("access_token");

        setIsLoggedIn(false);

        setMessage(
          "Session expired. Please login again."
        );

      } else {
        setMessage(
          "Failed to load claims."
        );
      }
    }
  };


  // ============================================================
  // LOGOUT
  // ============================================================

  const handleLogout = () => {
    localStorage.removeItem("access_token");

    setIsLoggedIn(false);

    setClaims([]);

    setMessage("Logged out successfully.");
  };


  // ============================================================
  // FORM CHANGE
  // ============================================================

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    });
  };


  // ============================================================
  // CREATE CLAIM + AI ANALYSIS
  // ============================================================

  const handleSubmit = async (event) => {
    event.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const token =
        localStorage.getItem("access_token");

      const response = await axios.post(
        `${API_URL}/claims`,
        {
          policy_number: formData.policy_number,
          claim_amount: Number(formData.claim_amount),
          hospital_name: formData.hospital_name,
          diagnosis: formData.diagnosis
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setMessage(response.data.message);

      // Store newly created claim
      // together with AI analysis results

      const newClaim = {
        _id: response.data.claim_id,

        policy_number:
          formData.policy_number,

        claim_amount:
          Number(formData.claim_amount),

        hospital_name:
          formData.hospital_name,

        diagnosis:
          formData.diagnosis,

        status: "Pending",

        fraud_risk_score:
          response.data.analysis.fraud_risk_score,

        fraud_risk_level:
          response.data.analysis.fraud_risk_level,

        decision:
          response.data.analysis.decision
      };

      setClaims((previousClaims) => [
        ...previousClaims,
        newClaim
      ]);

      // Clear form

      setFormData({
        policy_number: "",
        claim_amount: "",
        hospital_name: "",
        diagnosis: ""
      });

    } catch (error) {
      console.error(error);

      if (error.response?.status === 401) {

        localStorage.removeItem(
          "access_token"
        );

        setIsLoggedIn(false);

        setMessage(
          "Session expired. Please login again."
        );

      } else if (error.response) {

        setMessage(
          error.response.data.detail ||
          "Failed to submit claim"
        );

      } else {

        setMessage(
          "Unable to connect to the server"
        );
      }

    } finally {
      setLoading(false);
    }
  };


  // ============================================================
  // LOGIN PAGE
  // ============================================================

  if (!isLoggedIn) {
    return (
      <div>

        <h1>ClaimSense AI</h1>

        <h2>
          Insurance Claims Automation
        </h2>

        <h3>Login</h3>

        <form onSubmit={handleLogin}>

          <div>
            <label>
              Username
            </label>

            <br />

            <input
              type="text"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
              required
            />
          </div>

          <br />

          <div>
            <label>
              Password
            </label>

            <br />

            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />
          </div>

          <br />

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Logging in..."
              : "Login"}
          </button>

        </form>

        {message && (
          <p>{message}</p>
        )}

      </div>
    );
  }


  // ============================================================
  // DASHBOARD
  // ============================================================

  return (
    <div>

      <h1>ClaimSense AI</h1>

      <h2>
        Insurance Claims Automation
      </h2>

      <button onClick={handleLogout}>
        Logout
      </button>

      <hr />


      {/* ======================================================
          SUBMIT CLAIM
          ====================================================== */}

      <h3>
        Submit Insurance Claim
      </h3>

      <form onSubmit={handleSubmit}>

        <div>

          <label>
            Policy Number
          </label>

          <br />

          <input
            type="text"
            name="policy_number"
            value={formData.policy_number}
            onChange={handleChange}
            required
          />

        </div>

        <br />

        <div>

          <label>
            Claim Amount
          </label>

          <br />

          <input
            type="number"
            name="claim_amount"
            value={formData.claim_amount}
            onChange={handleChange}
            required
          />

        </div>

        <br />

        <div>

          <label>
            Hospital Name
          </label>

          <br />

          <input
            type="text"
            name="hospital_name"
            value={formData.hospital_name}
            onChange={handleChange}
            required
          />

        </div>

        <br />

        <div>

          <label>
            Diagnosis
          </label>

          <br />

          <input
            type="text"
            name="diagnosis"
            value={formData.diagnosis}
            onChange={handleChange}
            required
          />

        </div>

        <br />

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Submit Claim"}
        </button>

      </form>


      {/* ======================================================
          MESSAGE
          ====================================================== */}

      {message && (
        <h3>{message}</h3>
      )}


      <hr />


      {/* ======================================================
          MY CLAIMS
          ====================================================== */}

      <h3>
        My Claims
      </h3>

      <button onClick={fetchClaims}>
        Load Claims
      </button>


      {/* ======================================================
          CLAIM LIST
          ====================================================== */}

      {claims.length > 0 && (

        <div>

          {claims.map((claim) => (

            <div key={claim._id}>

              <p>
                <strong>
                  Policy:
                </strong>{" "}
                {claim.policy_number}
              </p>

              <p>
                <strong>
                  Amount:
                </strong>{" "}
                ₹{claim.claim_amount}
              </p>

              <p>
                <strong>
                  Hospital:
                </strong>{" "}
                {claim.hospital_name}
              </p>

              <p>
                <strong>
                  Diagnosis:
                </strong>{" "}
                {claim.diagnosis}
              </p>

              <p>
                <strong>
                  Status:
                </strong>{" "}
                {claim.status || "Pending"}
              </p>


              {/* ==================================================
                  AI FRAUD ANALYSIS
                  ================================================== */}

              <h4>
                AI Fraud Analysis
              </h4>

              <p>
                <strong>
                  Fraud Risk Score:
                </strong>{" "}
                {claim.fraud_risk_score ??
                  "Not available"}
              </p>

              <p>
                <strong>
                  Risk Level:
                </strong>{" "}
                {claim.fraud_risk_level ??
                  "Not available"}
              </p>

              <p>
                <strong>
                  AI Decision:
                </strong>{" "}
                {claim.decision ??
                  "Not available"}
              </p>

              <hr />

            </div>

          ))}

        </div>

      )}

    </div>
  );
}

export default App;