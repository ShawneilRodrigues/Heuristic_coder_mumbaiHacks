import React from "react";
import "./MainPage.css"; // Import CSS for styling\
import myimg from "./img.webp";
import { CiCalculator2 } from "react-icons/ci";
import { Link } from "react-router-dom";
const MainPage = () => {
  return (
    <div className="mainpage">
      {/* <Link
        style={{ height: "5rem", display: "inline-block", width: "5rem",border:"2px solid black",boxShadow:"2px solid",borderRadius:"100%",padding:"1rem" }}
        to={"/user"}
      >
        <CiCalculator2
          style={{ color: "#000", height: "100%", width: "100%" }}
        />
      </Link> */}
      {/* import { Link } from 'react-router-dom'; */}
{/* import { CiCalculator2 } from 'react-icons/ci'; */}

<Link
  style={{
    height: "5rem",
    width: "5rem",
    border: "2px solid #000",
    borderRadius: "50%",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    textDecoration: "none",
    color: "#000",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
    transition: "transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease",
  }}
  to="/user"
  onMouseEnter={(e) => {
    e.currentTarget.style.backgroundColor = "#a9e63d";
    e.currentTarget.style.transform = "scale(1.1)";
    e.currentTarget.style.boxShadow = "0 6px 12px rgba(0, 0, 0, 0.3)";
  }}
  onMouseLeave={(e) => {
    e.currentTarget.style.backgroundColor = "#fff";
    e.currentTarget.style.transform = "scale(1)";
    e.currentTarget.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
  }}
>
  <CiCalculator2 style={{ color: "#000", height: "70%", width: "70%" }} />
</Link>


      {/* <img src={myimg} width={"100%"}/> */}
    </div>
  );
};

export default MainPage;
