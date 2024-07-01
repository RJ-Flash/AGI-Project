import os
import subprocess
import requests
import pandas as pd
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
from knowledge_representation.ontology import Ontology
from knowledge_representation.symbolic_reasoning import SymbolicReasoning
from machine_learning.supervised_learning import SupervisedLearning
from nlp.language_understanding import LanguageUnderstanding
from rag.retriever import Retriever
from rag.generator import Generator

def download_file(url, local_filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except Exception as e:
        return str(e)

def download_model(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Failed to download model: {e.stderr.decode('utf-8')}"

def run_docker_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Failed to run command: {e.stderr.decode('utf-8')}"

def main():
    print("Welcome to the AGI Project Interactive Chat!")
    print("You can interact with different components of the system.")
    print("Type '/bye' to exit the chat.")
    print("Type 'help' to see available commands.")

    ontology = Ontology()
    symbolic_reasoning = SymbolicReasoning()
    supervised_learning = SupervisedLearning()
    language_understanding = LanguageUnderstanding()
    retriever = Retriever()
    generator = Generator()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "/bye":
            print("Goodbye!")
            break

        elif user_input.lower() == "help":
            response = ("Available commands:\n"
                        "- ontology <concept> <description>\n"
                        "- reason <premise>\n"
                        "- train <file_path_or_url>\n"
                        "- download <model_command>\n"
                        "- docker <command>\n"
                        "- predict <data_point_1> <data_point_2> ...\n"
                        "- understand <text>\n"
                        "- retrieve <query>\n"
                        "- generate <context>")

        elif user_input.lower().startswith("ontology"):
            try:
                _, concept, description = user_input.split(maxsplit=2)
                ontology.add_concept(concept, description)
                response = f"Ontology added: {concept} - {description}"
            except ValueError:
                response = "Invalid command format. Use: ontology <concept> <description>"

        elif user_input.lower().startswith("reason"):
            try:
                _, premise = user_input.split(maxsplit=1)
                symbolic_reasoning.add_premise(premise)
                response = f"Reasoning on premise '{premise}': {symbolic_reasoning.reason([premise.split()[0]])}"
            except ValueError:
                response = "Invalid command format. Use: reason <premise>"

        elif user_input.lower().startswith("train"):
            try:
                _, file_path_or_url = user_input.split(maxsplit=1)
                
                if file_path_or_url.startswith('http://') or file_path_or_url.startswith('https://'):
                    file_path = download_file(file_path_or_url, 'downloaded_training_data.csv')
                else:
                    file_path = file_path_or_url

                if not os.path.exists(file_path):
                    response = f"Error in training: File not found at {file_path}"
                else:
                    # Load training data for supervised learning
                    df = pd.read_csv(file_path)
                    data = df[['feature']].values.tolist()
                    labels = df['label'].values.tolist()
                    supervised_learning.train(data, labels)
                    
                    # Fine-tune GPT-2 on custom data
                    model_name = "gpt2"
                    model = GPT2LMHeadModel.from_pretrained(model_name)
                    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

                    def load_dataset(tokenizer, file_path, block_size=128):
                        return TextDataset(
                            tokenizer=tokenizer,
                            file_path=file_path,
                            block_size=block_size)

                    def data_collator(tokenizer):
                        return DataCollatorForLanguageModeling(
                            tokenizer=tokenizer,
                            mlm=False)

                    train_dataset = load_dataset(tokenizer, file_path)
                    training_args = TrainingArguments(
                        output_dir="./results",
                        overwrite_output_dir=True,
                        num_train_epochs=1,
                        per_device_train_batch_size=4,
                        save_steps=10_000,
                        save_total_limit=2,
                    )

                    trainer = Trainer(
                        model=model,
                        args=training_args,
                        data_collator=data_collator(tokenizer),
                        train_dataset=train_dataset,
                    )

                    trainer.train()

                    response = "Supervised learning model and LLM fine-tuned on provided data."
            except Exception as e:
                response = f"Error in training: {e}"

        elif user_input.lower().startswith("download"):
            try:
                _, model_command = user_input.split(maxsplit=1)
                response = download_model(model_command)
            except ValueError:
                response = "Invalid command format. Use: download <model_command>"

        elif user_input.lower().startswith("docker"):
            try:
                _, docker_command = user_input.split(maxsplit=1)
                response = run_docker_command(docker_command)
            except ValueError:
                response = "Invalid command format. Use: docker <command>"

        elif user_input.lower().startswith("predict"):
            try:
                _, *data_points = user_input.split()
                data_points = [[int(point)] for point in data_points]
                predictions = supervised_learning.predict(data_points)
                response = f"Predictions: {predictions}"
            except ValueError:
                response = "Invalid command format. Use: predict <data_point_1> <data_point_2> ..."

        elif user_input.lower().startswith("understand"):
            try:
                _, text = user_input.split(maxsplit=1)
                result = language_understanding.understand(text)
                response = f"Language understanding result: {result}"
            except ValueError:
                response = "Invalid command format. Use: understand <text>"

        elif user_input.lower().startswith("retrieve"):
            try:
                _, query = user_input.split(maxsplit=1)
                retriever.add_documents(["AGI is the future", "Machine learning is a subset of AGI"])
                retrieved_docs = retriever.retrieve(query)
                response = f"Retrieved documents: {retrieved_docs}"
            except ValueError:
                response = "Invalid command format. Use: retrieve <query>"

        elif user_input.lower().startswith("generate"):
            try:
                _, context = user_input.split(maxsplit=1)
                generated_text = generator.generate(context)
                response = f"Generated text: {generated_text}"
            except ValueError:
                response = "Invalid command format. Use: generate <context>"

        else:
            response = "Sorry, I didn't understand that command. Type 'help' to see available commands."

        print(f"AGI: {response}")

if __name__ == "__main__":
    main()
