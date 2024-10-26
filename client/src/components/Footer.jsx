import React from "react";
import "./Footer.css";
import EcoTrackLogo from "./EcoTrackLogo";
import { Link } from "react-router-dom";
import {AiOutlineCopyright,AiOutlineLinkedin,AiOutlineInstagram,AiOutlineGithub,AiOutlineSend} from "react-icons/ai"
import mg from "./img2.png"
const Footer = () => {
  return (
    <div className="footer">
      <div className="copyright">&copy; All Rights Reserved</div>
        <div className="text">
            {/* <Link to={"/user"}><CiCalculator2 style={{color:"white",}}/></Link>     */}
    <img src={mg} height={"2rem"}/>
   
        </div>
   
        
      <div className="contact">
  {/* <h2>Contact Us</h2> */}
  <a href="https://www.linkedin.com/in/saurabhkumar-sharma-687767298" target='blank'><AiOutlineLinkedin/>LinkedIn</a>
<a href="https://github.com/saurabhk1410" target='blank'><AiOutlineGithub/>Github</a>
<a href="https://instagram.com/saurabh._.3" target='blank'><AiOutlineInstagram/>Instagram</a>
      </div>
    </div>
  );
};

export default Footer;
