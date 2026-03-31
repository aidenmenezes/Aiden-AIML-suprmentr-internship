import dotenv from "dotenv";
import readline from "readline";
import axios from "axios";

dotenv.config();

const GROQ_API_KEY = process.env.GROQ_API_KEY;
if (!GROQ_API_KEY) {
  console.error("Missing GROQ_API_KEY environment variable. Please add it to .env or set it in your shell.");
  process.exit(1);
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function askQuestion(query) {
  return new Promise((resolve) => {
    rl.question(query, (answer) => {
      resolve(answer);
    });
  });
}

async function main() {
  const topic = await askQuestion("Enter a topic for AI Study Assistant: ");

  const userPrompt = `Explain ${topic} in simple terms, include a short example and a few key points.`;

  const requestBody = {
    model: "llama-3.1-8b-instant",
    messages: [{ role: "user", content: userPrompt }],
  };

  try {
    const response = await axios.post(
      "https://api.groq.com/openai/v1/chat/completions",
      requestBody,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${GROQ_API_KEY}`,
        },
      }
    );

    const explanation =
      response.data?.choices?.[0]?.message?.content ||
      response.data?.choices?.[0]?.text ||
      JSON.stringify(response.data, null, 2);

    console.log("\n=== AI Study Assistant Response ===\n");
    console.log(explanation);
  } catch (err) {
    console.error("Error generating AI explanation:", err.response ? err.response.data : err.message);
  } finally {
    rl.close();
  }
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});