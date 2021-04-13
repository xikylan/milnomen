import React, { useState, useEffect } from "react";
import {
  Jumbotron,
  Container,
  Button,
  Spinner,
  ListGroup,
} from "react-bootstrap";
import WordDisplay from "./WordDisplay";
import SentenceItem from "./SentenceItem";

import styles from "./styles/WordSelector.module.css";

export default function WordSelector({ srcLang, destLang }) {
  const [rank, setRank] = useState(0);
  const [words, setWords] = useState([]);
  const [sentences, setSentences] = useState([]);
  const [firstLoad, setFirstLoad] = useState(true);

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
          setSentences((oldArray) => [...oldArray, ...data.data.sentences]);
          console.log("Length " + sentences.length);
        });
    }
    if (firstLoad) {
      setFirstLoad(false);
      getSentences();
    } else if (rank === sentences.length - 1) {
      getSentences();
    }
  }, [srcLang, rank, sentences.length, firstLoad]);

  return (
    <>
      {words.length && sentences.length ? (
        <>
          <Jumbotron fluid>
            <Container>
              <WordDisplay word={words[rank]} />
              <div className={styles.btnContainer}>
                <Button
                  className={styles.selectBtn}
                  disabled={rank > 0 ? false : true}
                  onClick={() => (rank > 0 ? setRank(rank - 1) : setRank(0))}
                >
                  &lt;
                </Button>
                <Button
                  className={styles.selectBtn}
                  onClick={() => setRank(rank + 1)}
                >
                  &gt;
                </Button>
              </div>
            </Container>
          </Jumbotron>
          <Container>
            <h4>Examples</h4>
            <ListGroup variant="flush">
              {sentences[rank].text.map((sen, key) => {
                return (
                  <SentenceItem
                    sentence={sen}
                    translation={sentences[rank].translations[key]}
                    rank={key + 1}
                    key={key}
                  />
                );
              })}
            </ListGroup>
          </Container>
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
