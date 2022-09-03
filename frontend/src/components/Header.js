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

      <div>
        <h3>
          <Link to = "/">
            <BsFillHouseFill/>
          </Link>
        </h3>
      </div>

      <div>
        <div>
          <h1>
            Deep Atomas
          </h1>
        </div>
      </div>

      <div onClick = {openModal}>
        <h3>
          <div>
            <BsInfoCircleFill/>
          </div>
        </h3>
      </div>

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
            This is super cool, trust me.
          </div>

          <div className = "info-modal-entry">
            <h3>
              How do I play?

            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Just get good.
          </div>

          <div className = "info-modal-entry">
            <h3>
              What's so deep about Deep Atomas?
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Deep Q Learning.
          </div>

          <div className = "info-modal-entry">
            <h3>
              Where can I play the original Atomas?
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Google Play Store. Thanks Max Gittel!
          </div>

        </div>

      </Modal>

    </div>
  )
}

export default Header