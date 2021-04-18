import React from "react";
import { Spinner } from "react-bootstrap";
import styles from "./styles/LoadingScreen.module.css";

export default function LoadingScreen() {
  return (
    <div className={styles.loading}>
      <Spinner className={styles.spinner} animation="grow" size="sm" />
      <Spinner className={styles.spinner} animation="grow" size="sm" />
      <Spinner className={styles.spinner} animation="grow" size="sm" />
    </div>
  );
}
