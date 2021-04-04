import React, { useState, useEffect } from "react";
import { Container, Jumbotron, Table, Button } from "react-bootstrap";
import NavigationBar from "./homepage/NavigationBar";

import styles from "./homepage/styles/SpanishPage.module.css";

export default function SpanishPage() {
  const [words, setWords] = useState([]);

  useEffect(() => {
    fetch("/api/es/words")
      .then((res) => res.json())
      .then((data) => {
        setWords([...data.data.words]);
        console.log(words);
      });
  }, []);

  return (
    <>
      <NavigationBar />
      <Jumbotron fluid className={styles.jumbo}>
        <Container>
          <h1>Top 1000 Spanish words</h1>
          <p>Source: Open Subtitles 2018</p>
          <Button className={styles.studybtn}>Study list</Button>
        </Container>
      </Jumbotron>
      <Container>
        <Table striped borderless size="sm">
          <thead>
            <tr>
              <th>#</th>
              <th>Spanish</th>
              <th>English</th>
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
      </Container>
    </>
  );
}
