import React, { useState, useEffect } from "react";
import { Table } from "react-bootstrap";
import styles from "./styles/WordTable.module.css";

export default function WordTable({ srcLang, destLang }) {
  const [words, setWords] = useState([]);

  useEffect(() => {
    function getWords() {
      fetch(`/api/${srcLang}/words`)
        .then((res) => res.json())
        .then((data) => {
          setWords([...data.data.words]);
        });
    }
    getWords();
  }, [srcLang]);

  return (
    <Table striped borderless size="sm">
      <thead>
        <tr className={styles.tableheader}>
          <th>#</th>
          <th>{srcLang}</th>
          <th>{destLang}</th>
        </tr>
      </thead>
      <tbody className={styles.tablebody}>
        {words.map((word, key) => {
          return (
            <tr key={key}>
              <td>{word.rank}</td>
              <td>{word.text}</td>
              <td>{word.translations.slice(0, 3).join(", ")}</td>
            </tr>
          );
        })}
      </tbody>
    </Table>
  );
}
