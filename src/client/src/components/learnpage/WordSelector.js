import React, { useState, useEffect } from "react";
import {
  Container,
  Button,
  Spinner,
  ListGroup,
  ProgressBar,
} from "react-bootstrap";
import WordDisplay from "./WordDisplay";
import SentenceItem from "./SentenceItem";

import styles from "./styles/WordSelector.module.css";

export default function WordSelector({ srcLang, destLang }) {
  const [rank, setRank] = useState(0);
  const [words, setWords] = useState([]);
  const [sentences, setSentences] = useState([]);
  const [firstLoad, setFirstLoad] = useState(true);

  const maxRank = 999;

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

  useEffect(() => {
    function getSentences() {
      fetch(`/api/${srcLang}/sentences/${sentences.length}`)
        .then((res) => res.json())
        .then((data) => {
          console.log(rank);
          setSentences((oldArray) => [...oldArray, ...data.data.sentences]);
        });
    }
    if (firstLoad) {
      setFirstLoad(false);
      getSentences();
    } else if (rank === sentences.length - 5) {
      getSentences();
    }
  }, [srcLang, rank, sentences.length, firstLoad]);

  return (
    <>
      {words.length && sentences.length ? (
        <>
          <ProgressBar
            variant="warning"
            className={styles.progress}
            now={(rank * 100) / words.length}
          />
          <div className={styles.headerContainer}>
            <WordDisplay word={words[rank]} />
            <div className={styles.btnContainer}>
              <Button
                size="lg"
                variant="light"
                className={styles.selectBtn}
                disabled={rank > 0 ? false : true}
                onClick={() => (rank > 0 ? setRank(rank - 1) : setRank(0))}
              >
                Back
              </Button>
              <Button
                size="lg"
                variant="warning"
                className={styles.selectBtn}
                disabled={rank < maxRank ? false : true}
                onClick={() =>
                  rank < maxRank ? setRank(rank + 1) : setRank(maxRank)
                }
              >
                Next
              </Button>
            </div>
            <hr />
          </div>
          <div>
            <h4 style={{ fontSize: "1.3rem" }}>Examples</h4>
            <ListGroup variant="flush">
              {sentences[rank].text.map((text, key) => {
                return (
                  <SentenceItem
                    sentence={text}
                    translation={sentences[rank].translations[key]}
                    rank={key + 1}
                    key={key}
                  />
                );
              })}
            </ListGroup>
          </div>
        </>
      ) : (
        <div>
          Loading
          <Spinner animation="border" />
        </div>
      )}
    </>
  );
}
