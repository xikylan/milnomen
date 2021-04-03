import React from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import { ReactComponent as SpainLogo } from "../../assets/spain.svg";
import { ReactComponent as FranceLogo } from "../../assets/france.svg";

export default function ChooseLanguage() {
  return (
    <div style={{ backgroundColor: "#f8f8f8" }}>
      <Container>
        <p
          style={{
            textAlign: "center",
            fontSize: 25,
            marginBottom: 60,
            paddingTop: "1rem",
          }}
        >
          Choose a language
        </p>
      </Container>

      <Container>
        <Row>
          <Col>
            <Button
              expand="lg"
              variant="light"
              style={{
                height: 120,
                width: 120,
              }}
            >
              <SpainLogo style={{ width: "60%", height: "60%", margin: 10 }} />
              <p>Spanish</p>
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
