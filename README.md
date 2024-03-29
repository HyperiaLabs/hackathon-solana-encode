<div align="center">
  
  <img src="https://avatars.githubusercontent.com/u/150239758?s=100" width="100" />
  
  <br>
  
  <p>
    A behavioral prediction tool based on on-chain activities, leveraging artificial intelligence.
  </p>

  <p>
    <a href="https://mathis-hyperia-labs.notion.site/Solana-x-Encode-Hackaton-Hyperia-Labs-2ca5f80b93f1402a8ab1244b53ad0541">Notion</a>   
    •
    <a href="https://youtu.be/ELASbgihVIQ">Youtube</a>    
    •
    <a href="https://file.notion.so/f/f/0f9812f2-badf-4065-a87c-47e47dfb21a1/b9a6bb20-a5a7-4f60-9e80-c5b1850fd6ff/Wallet_Clustering_-_Technical_Paper.pdf?id=e8ddf03c-5566-41e1-a02e-6edd1be81c9b&table=block&spaceId=0f9812f2-badf-4065-a87c-47e47dfb21a1&expirationTimestamp=1707163200000&signature=WX590s0a620dgw25Hx4T5ezsO1YdH6l5-ACjkNpiifU&downloadName=Wallet+Clustering+-+Technical+Paper.pdf">Wallet Clustering - Technical Paper</a>    
    •
    <a href="https://file.notion.so/f/f/0f9812f2-badf-4065-a87c-47e47dfb21a1/fa113cde-adf4-4a2f-90c0-efbf86926623/Behavioral_Prediction_-_Technical_Paper.pdf?id=c98b730c-4a88-4243-b28e-89e64380cd3e&table=block&spaceId=0f9812f2-badf-4065-a87c-47e47dfb21a1&expirationTimestamp=1707163200000&signature=KN-BZiOtvDEXsCxVddMOgQW0mV0_7p-gRkn6Y1LXHUM&downloadName=Behavioral+Prediction+-+Technical+Paper.pdf">Behavioral Prediction - Technical Paper</a>    
  </p>
  
</div>

<hr>

# Hyperia Labs Behavioral Prediction Tool

This is our participation in the [Solana x Encode Hackaton](https://www.encode.club/encodesolanahack)!

## Overview

Hyperia Labs presents an advanced Behavioral Prediction. Tool that employs Deep Learning, Deep Neural network and Blockchain analytics to provide predictive insights into user behaviors. By analyzing on-chain data, the tool can adeptly anticipates market trends and user behavior. This comprehensive tool not only deciphers current user interactions but also sets a new standard in forecasting future activities within the blockchain space, making it an indispensable asset for investors, project owners and analysts alike.

All of our content created for the hackathon can be accessed on [this Notion page](https://mathis-hyperia-labs.notion.site/Solana-x-Encode-Hackaton-Hyperia-Labs-2ca5f80b93f1402a8ab1244b53ad0541), including videos, pitch decks, technical paper and more.

## Where can I start reviewing this project?

### Getting data to train the IA
To train our AI, we used data from all wallets that had interactions with the blockchain during September 1, 2023, to November 30, 2023 (3 months). We get only 1 Go of data because the total for all wallets have interact during this 3 months is equal to 4 000 Go. This is enough to train a first AI model but for more reliability we will need more resources.

All of the scripts used to get the data can be found in the [extract-data folder](https://github.com/HyperiaLabs/solana-hackathon-encode/tree/main/scripts/extract-data)

### Data
The AI model was trained on a dataset comprising 1 GB of blockchain transaction data from a three-month period, considered adequate for an initial model. Scripts in the extract-data folder facilitated data extraction. Transactions were categorized (e.g., real estate, DeFi, NFT) for in-depth analysis and predictive modeling. Additional data is expected to improve the model's accuracy. You can check the [data part](https://github.com/HyperiaLabs/solana-hackathon-encode/tree/main/scripts/data)

### AI Model
It's a Bayesian LSTM model to predict blockchain wallet behavior by analyzing time-series data. The model treats parameters as probability distributions and employs variational inference to approximate complex posterior distributions, enabling it to make probabilistic predictions about future wallet activities. This AI model has been initially validated using synthetic data, with real-world data applications anticipated to be more complex.

You can check the [AI models](https://github.com/HyperiaLabs/solana-hackathon-encode/tree/main/scripts/ai) and the technical papers :
- [Wallet Clustering](https://file.notion.so/f/f/0f9812f2-badf-4065-a87c-47e47dfb21a1/b9a6bb20-a5a7-4f60-9e80-c5b1850fd6ff/Wallet_Clustering_-_Technical_Paper.pdf?id=e8ddf03c-5566-41e1-a02e-6edd1be81c9b&table=block&spaceId=0f9812f2-badf-4065-a87c-47e47dfb21a1&expirationTimestamp=1707163200000&signature=WX590s0a620dgw25Hx4T5ezsO1YdH6l5-ACjkNpiifU&downloadName=Wallet+Clustering+-+Technical+Paper.pdf)
- [Behavioral Prediction](https://file.notion.so/f/f/0f9812f2-badf-4065-a87c-47e47dfb21a1/fa113cde-adf4-4a2f-90c0-efbf86926623/Behavioral_Prediction_-_Technical_Paper.pdf?id=c98b730c-4a88-4243-b28e-89e64380cd3e&table=block&spaceId=0f9812f2-badf-4065-a87c-47e47dfb21a1&expirationTimestamp=1707163200000&signature=KN-BZiOtvDEXsCxVddMOgQW0mV0_7p-gRkn6Y1LXHUM&downloadName=Behavioral+Prediction+-+Technical+Paper.pdf)
