import { DiscordSDK } from '@discord/embedded-app-sdk'

export const sdk = new DiscordSDK(import.meta.env.VITE_DISCORD_CLIENT_ID)

export async function authorize(): Promise<string> {
  const { code } = await sdk.commands.authorize({
    client_id: sdk.clientId,
    response_type: 'code',
    state: '',
    prompt: 'none',
    scope: ['identify', 'guilds'],
  })
  return code
}
