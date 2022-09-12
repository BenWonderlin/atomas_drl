import React from 'react'
import { BsFillHouseFill, BsInfoCircleFill } from "react-icons/bs"
import { Link } from "react-router-dom"

const Header = () => {

  return (
    
    <div className = "app-header">

      <h3>
        <Link to = "/">
          <BsFillHouseFill/>
        </Link>
      </h3>

      <div>
        <h1>
          Deep Atomas
        </h1>
      </div>

      <h3>
        <Link to = "/info">
          <BsInfoCircleFill/>
        </Link>
      </h3>
  
    </div>

  )
}

export default Header