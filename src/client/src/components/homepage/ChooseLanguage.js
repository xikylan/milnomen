import React from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import { ReactComponent as SpainLogo } from "../../assets/spain.svg";
import { ReactComponent as FranceLogo } from "../../assets/france.svg";
import styles from "./styles/ChooseLanguage.module.css";

import LanguageButton from "./LanguageButton";

export default function ChooseLanguage() {
  return (
    <div className={styles.container}>
      <Container>
        <p className={styles.heading}>Choose a language</p>
      </Container>

      <Container>
        <Row>
          <Col>
            <LanguageButton name="prague" />
          </Col>
          <Col>
            <Button
              variant="light"
              style={{
                height: 120,
                width: 120,
              }}
            >
              <SpainLogo style={{ width: "60%", height: "60%", margin: 10 }} />
              <p>French</p>
            </Button>
          </Col>
          <Col>
            <Button
              variant="light"
              style={{
                height: 120,
                width: 120,
              }}
            >
              <FranceLogo style={{ width: "60%", height: "60%", margin: 10 }} />
              <p>French</p>
            </Button>
          </Col>
          <Col>
            <Button
              variant="light"
              style={{
                height: 120,
                width: 120,
              }}
            >
              <FranceLogo style={{ width: "60%", height: "60%", margin: 10 }} />
              <p>French</p>
            </Button>
          </Col>
          <Col>
            <Button
              variant="light"
              style={{
                height: 120,
                width: 120,
              }}
            >
              <FranceLogo style={{ width: "60%", height: "60%", margin: 10 }} />
              <p>French</p>
            </Button>
          </Col>
          <Col>
            <Button
              variant="light"
              style={{
                height: 120,
                width: 120,
              }}
            >
              <FranceLogo style={{ width: "60%", height: "60%", margin: 10 }} />
              <p>French</p>
            </Button>
          </Col>
          <Col>
            <Button
              variant="light"
              style={{
                height: 120,
                width: 120,
              }}
            >
              <FranceLogo style={{ width: "60%", height: "60%", margin: 10 }} />
              <p>French</p>
            </Button>
          </Col>
          <Col>
            <Button
              variant="light"
              style={{
                height: 120,
                width: 120,
              }}
            >
              <FranceLogo style={{ width: "60%", height: "60%", margin: 10 }} />
              <p>French</p>
            </Button>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
