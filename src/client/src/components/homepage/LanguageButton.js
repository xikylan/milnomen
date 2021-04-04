import React, { useState, useEffect } from "react";
import { Button, Image } from "react-bootstrap";

import styles from "./styles/LanguageButton.module.css";

export default function LanguageButton({ name }) {
  return (
    <Button variant="light" className={styles.btn}>
      <Image src={import("../../assets/" + name + ".jpg")} thumbnail />
      <p>{name}</p>
    </Button>
  );
}
