import React from "react";
import { ListGroup } from "react-bootstrap";

import styles from "./styles/SentenceItem.module.css";

export default function SentenceItem({ sentence, translation, rank }) {
  return (
    <ListGroup.Item key={rank}>
      <div>
        <p className={styles.rank}>#{rank}</p>
        <p className={styles.sentence}>{sentence}</p>
        <p className={styles.translation}>{translation}</p>
      </div>
    </ListGroup.Item>
  );
}
