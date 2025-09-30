use ethers::{prelude::*, utils::parse_units};
use dotenv::dotenv;
use std::{env, sync::Arc};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    dotenv().ok();

    let rpc_url = env::var("RPC_URL")?;
    let private_key = env::var("PRIVATE_KEY")?;
    let token_address: Address = env::var("TOKEN_ADDRESS")?.parse()?;

    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        println!("Usage: mint <wallet_address> <amount>");
        return Ok(());
    }

    let to_address: Address = args[1].parse()?;
    let amount: U256 = parse_units(&args[2], 18)?.into();  // 18 decimals

    // Setup provider and wallet
    let provider = Provider::<Http>::try_from(rpc_url)?;
    let wallet = private_key.parse::<LocalWallet>()?;
    let client = SignerMiddleware::new(provider, wallet);
    let client = Arc::new(client);

    // Load contract with correct ABI
    let abi: ethers::abi::Abi = serde_json::from_str(include_str!("../abi/erc20.json"))?;
    let contract = Contract::new(token_address, abi, client.clone());

    // Call the correct method: "mint" instead of "transfer"
    let method = contract.method::<_, H256>("mint", (to_address, amount))?;
    let tx = method.send().await?;

    println!("✅ Minted tokens to {} | Tx: {:?}", args[1], tx.tx_hash());
    Ok(())
}
