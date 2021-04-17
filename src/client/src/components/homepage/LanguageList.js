import React, { useEffect, useState } from "react";
import { Container, ListGroup } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./styles/LanguageList.module.css";

export default function LanguageList() {
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    function getLanguages() {
      fetch("/api/languages")
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          setLanguages([...data.data.languages]);
        });
    }
    getLanguages();
  }, []);

  return (
    <>
      <Container className={styles.container}>
        <p className={styles.heading}>Choose a language</p>
        <Container className={styles.langlist}>
          <ListGroup variant="flush">
            {languages.map((lang, key) => {
              return (
                <Link key={key} className="langtext" to={`/${lang}`}>
                  {lang}
                </Link>
              );
            })}
            <ListGroup.Item action></ListGroup.Item>
          </ListGroup>
        </Container>
      </Container>
    </>
  );
}
