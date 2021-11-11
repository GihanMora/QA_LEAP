import datetime
from transformers import TapasTokenizer, TapasForQuestionAnswering
import pandas as pd
import torch

def load_model_and_tokenizer():
    """
      Load
    """
    # Load pretrained tokenizer: TAPAS finetuned on WikiTable Questions
    tokenizer = TapasTokenizer.from_pretrained("google/tapas-base-finetuned-wtq")

    # Load pretrained model: TAPAS finetuned on WikiTable Questions
    model = TapasForQuestionAnswering.from_pretrained("google/tapas-base-finetuned-wtq")

    # Return tokenizer and model
    return tokenizer, model


def prepare_inputs(data, queries, tokenizer):
    """
      Convert dictionary into data frame and tokenize inputs given queries.
    """
    # Prepare inputs
    table = pd.DataFrame.from_dict(data)
    inputs = tokenizer(table=table, queries=queries,truncation=True, padding=True,return_tensors="pt").to(device)

    # Return things
    return table, inputs


def generate_predictions(inputs, model, tokenizer):
    """
      Generate predictions for some tokenized input.
    """
    # Generate model results
    outputs = model(**inputs)

    # Convert logit outputs into predictions for table cells and aggregation operators
    predicted_table_cell_coords, predicted_aggregation_operators = tokenizer.convert_logits_to_predictions(
        inputs,
        outputs.logits.detach(),
        outputs.logits_aggregation.detach()
    )

    print(predicted_table_cell_coords)
    print(predicted_aggregation_operators)

    # Return values
    return predicted_table_cell_coords, predicted_aggregation_operators


def postprocess_predictions(predicted_aggregation_operators, predicted_table_cell_coords, table):
    """
      Compute the predicted operation and nicely structure the answers.
    """
    # Process predicted aggregation operators
    aggregation_operators = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
    aggregation_predictions_string = [aggregation_operators[x] for x in predicted_aggregation_operators]

    # Process predicted table cell coordinates
    answers = []
    for coordinates in predicted_table_cell_coords:
        if len(coordinates) == 1:
            # 1 cell
            answers.append(table.iat[coordinates[0]])
        else:
            # > 1 cell
            cell_values = []
            for coordinate in coordinates:
                cell_values.append(table.iat[coordinate])
            answers.append(", ".join(cell_values))

    # Return values
    return aggregation_predictions_string, answers


def show_answers(queries, answers, aggregation_predictions_string):
    """
      Visualize the postprocessed answers.
    """

    ans_list = []
    for query, answer, predicted_agg in zip(queries, answers, aggregation_predictions_string):
        print(query)
        print(answer,type(answer))
        print(predicted_agg)
        answer = [i.strip() for i in answer.split(',')]
        print(answer)
        if (len(answer) == 1):
            if (predicted_agg == 'COUNT'):
                answer = len([i for i in answer])

        if (len(answer) > 1):
            if (predicted_agg == 'SUM'):
                try:
                    answer = sum([float(i) for i in answer])
                except ValueError:
                    answer = predicted_agg
            elif (predicted_agg == 'COUNT'):
                answer = len([i for i in answer])
            elif (predicted_agg == 'AVERAGE'):
                answer = sum([float(i) for i in answer]) / len([i for i in answer])
            elif (predicted_agg == 'NONE'):
                answer = answer
            else:
                answer = 'None'
        # if predicted_agg == "NONE":
        #     print("Predicted answer: " + answer)
        # else:
        #     print("Predicted answer: " + predicted_agg + " > " + answer)

        ans_list.append(answer)

    return ans_list





def run_tapas(data, queries):
    """
      Invoke the TAPAS model.
    """
    tokenizer, model = load_model_and_tokenizer()
    table, inputs = prepare_inputs(data, queries, tokenizer)
    predicted_table_cell_coords, predicted_aggregation_operators = generate_predictions(inputs, model, tokenizer)
    aggregation_predictions_string, answers = postprocess_predictions(predicted_aggregation_operators,
                                                                      predicted_table_cell_coords, table)
    ans_list = show_answers(queries, answers, aggregation_predictions_string)

    print(ans_list)



if __name__ == '__main__':
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(device)
    table_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\building_data.csv")
    qa_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\question_answer_pairs.csv")
    # print(table_df.columns)
    # # Define the table
    table = {}
    #
    for c in table_df.columns:
        # if(c in ['Building', 'Total Energy Usage YTD','Total Energy Usage MTD', 'Total Energy Usage WTD','Cost Difference with Baseline', 'Estimated Total Cost','CO2 Emission YTD', 'Maximum Peak Energy Consumption']):
        if (c in ['Building', 'Total_Energy_Usage_YTD', 'Total_Energy_Usage_MTD', 'Total_Energy_Usage_WTD',
                  'Cost_Difference_with_Baseline', 'Estimated_Total_Cost', 'CO2_Emission_YTD',
                  'Maximum_Peak_Energy_Consumption']):
            table[c] = [str(i) for i in table_df[c].tolist()]
    data = table
    queries = qa_df['question'].tolist()
    # data = {'Cities': [str(i) for i in range(30)], 'Inhabitants': [str(i * 100) for i in range(30)]}

    # Define the questions
    # queries = ["Which city has most inhabitants?", "What is the average number of inhabitants?",
    #            "How many French cities are in the list?", "How many inhabitants live in French cities?"]
    for q in queries:
        predictions = run_tapas(data,[q])
        print(predictions)
        break

    out_df = qa_df
    out_df['predictions'] = predictions
    out_df.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\tapas\predictions\\predictions_script_tapas.csv")