import React, { useState, useEffect } from "react";
import { Button, ListGroup, ProgressBar } from "react-bootstrap";
import WordDisplay from "./WordDisplay";
import SentenceItem from "./SentenceItem";

import styles from "./styles/WordSelector.module.css";
import LoadingScreen from "../global/LoadingScreen";

export default function WordSelector({ srcLang, destLang }) {
  const [rank, setRank] = useState(0);
  const [words, setWords] = useState([]);
  const [sentences, setSentences] = useState([]);
  const [firstLoad, setFirstLoad] = useState(true);

  const maxRank = 999;

  useEffect(() => {
    fetch(`/api/${srcLang}/words`)
      .then((res) => res.json())
      .then((data) => {
        console.log("TRUE");
        setWords([...data.data.words]);
      })
      .catch((error) => console.log(error.message));
  }, [srcLang]);

  useEffect(() => {
    if (rank === sentences.length - 5 || firstLoad) {
      fetch(`/api/${srcLang}/sentences/${sentences.length}`)
        .then((res) => res.json())
        .then((data) => {
          console.log("TRUE");
          setSentences((oldArray) => [...oldArray, ...data.data.sentences]);
          setFirstLoad(false);
        })
        .catch((error) => console.log(error.message));
    }
  }, [srcLang, rank, sentences.length, firstLoad]);

  return (
    <>
      {words.length && sentences.length ? (
        <>
          <div className={styles.headerContainer}>
            <ProgressBar
              variant="warning"
              className={styles.progress}
              now={(rank * 100) / words.length}
            />
            <div>
              <WordDisplay
                word={words[rank]}
                srcLang={srcLang}
                destLang={destLang}
              />
            </div>
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
          </div>
          <hr />
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
          <LoadingScreen />
        </div>
      )}
    </>
  );
}
