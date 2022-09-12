import React from 'react'
import { BsFillHouseFill, BsInfoCircleFill } from "react-icons/bs"
import { Link } from "react-router-dom"
import * as Modal from "react-modal"

Modal.setAppElement("#root");

const Header = () => {

  const [modalIsOpen, setIsOpen] = React.useState(false);

  function openModal() {
    setIsOpen(true);
  }

  function afterOpenModal() {
  }

  function closeModal() {
    setIsOpen(false);
  }


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

      <h3 onClick = {openModal}>
        <div>
          <BsInfoCircleFill/>
        </div>
      </h3>

      <Modal
          isOpen = {modalIsOpen}
          onAfterOpen = {afterOpenModal}
          onRequestClose = {closeModal}
          className = {"info-modal"}
      >
        <div className = "info-modal-body">

          <h2>
            Welcome to Deep Atomas!
          </h2>

          <div className = "info-modal-subtitle">
            An AI-assisted implementation of the mobile game Atomas
          </div>

          <div className = "info-modal-entry">
            <h3>
              How do I play?
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Build symmetric patterns on the ring by placing the center atoms. 
            Place plus atoms on lines of symmetry to accumulate score and reduce your atom count.
            Leverage minus atoms to adjust the arrangement of your ring before you run out of space!
          </div>

          <div className = "info-modal-entry">
            <h3>
              What's so deep about Deep Atomas?
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Deep Atomas is equipped with an AI agent that used Deep Q Learning to study millions of games of Atomas.
            You can tap the brain button above the center atom to have Deep Atomas take a turn for you, but beware— 
            Deep Atomas is currently quite shallow. It averages about 75 points per game.
          </div>

          <div className = "info-modal-entry">
            <h3>
              Where can I play the original Atomas?
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Max Gittel's Atomas is available Google Play Store and the Apple App Store. It includes some features not implemented here. Check it out!
          </div>

        </div>

      </Modal>

    </div>
  )
}

export default Header