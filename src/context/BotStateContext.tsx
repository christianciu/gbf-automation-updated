import { createContext, useState } from "react"

export interface Settings {
    // Game settings.
    combatScriptName: string
    combatScript: string[]
    farmingMode: string
    item: string
    mission: string
    map: string
    itemAmount: number
    summons: string[]
    summonElements: string[]
    groupNumber: number
    partyNumber: number
    debugMode: boolean

    // Extra Settings.
    twitterAPIKey: string
    twitterAPIKeySecret: string
    twitterAccessToken: string
    twitterAccessTokenSecret: string
    enableDiscordNotifications: boolean
    discordToken: string
    discordUserID: string
    enableAutoRestore: boolean
    enableFullElixir: boolean
    enableSoulBalm: boolean
    enableBezierCurveMouseMovement: boolean
    mouseSpeed: number
    enableDelayBetweenRuns: boolean
    delayBetweenRuns: number
    enableRandomizedDelayBetweenRuns: boolean
    delayBetweenRunsLowerBound: number
    delayBetweenRunsUpperBound: number
    enableAutoExitRaid: boolean
    timeAllowedUntilAutoExitRaid: number
    enableNoTimeout: boolean

    // Extra Settings related to Nightmares from certain Farming Modes.
    enableNightmare: boolean
    enableCustomNightmareSettings: boolean
    nightmareCombatScriptName: string
    nightmareCombatScript: string[]
    nightmareSummons: string[]
    nightmareSummonElements: string[]
    nightmareGroupNumber: number
    nightmarePartyNumber: number

    enableStopOnArcarumBoss: boolean
}

// Set the default settings.
const defaultSettings: Settings = {
    combatScriptName: "",
    combatScript: [],
    farmingMode: "",
    item: "",
    mission: "",
    map: "",
    itemAmount: 1,
    summons: [],
    summonElements: [],
    groupNumber: 1,
    partyNumber: 1,
    debugMode: false,

    twitterAPIKey: "",
    twitterAPIKeySecret: "",
    twitterAccessToken: "",
    twitterAccessTokenSecret: "",
    enableDiscordNotifications: false,
    discordToken: "",
    discordUserID: "",
    enableAutoRestore: true,
    enableFullElixir: false,
    enableSoulBalm: false,
    enableBezierCurveMouseMovement: true,
    mouseSpeed: 0.2,
    enableDelayBetweenRuns: false,
    delayBetweenRuns: 15,
    enableRandomizedDelayBetweenRuns: false,
    delayBetweenRunsLowerBound: 15,
    delayBetweenRunsUpperBound: 60,
    enableAutoExitRaid: false,
    timeAllowedUntilAutoExitRaid: 10,
    enableNoTimeout: false,

    enableNightmare: false,
    enableCustomNightmareSettings: false,
    nightmareCombatScriptName: "",
    nightmareCombatScript: [],
    nightmareSummons: [],
    nightmareSummonElements: [],
    nightmareGroupNumber: 1,
    nightmarePartyNumber: 1,

    enableStopOnArcarumBoss: true,
}

interface IProviderProps {
    readyStatus: boolean
    setReadyStatus: (readyStatus: boolean) => void
    isBotRunning: boolean
    setIsBotRunning: (isBotRunning: boolean) => void
    startBot: boolean
    setStartBot: (startBot: boolean) => void
    stopBot: boolean
    setStopBot: (stopBot: boolean) => void
    refreshAlert: boolean
    setRefreshAlert: (refreshAlert: boolean) => void
    settings: Settings
    setSettings: (settings: Settings) => void
}

export const BotStateContext = createContext<IProviderProps>({} as IProviderProps)

// https://stackoverflow.com/a/60130448 and https://stackoverflow.com/a/60198351
export const BotStateProvider = ({ children }: any): JSX.Element => {
    const [readyStatus, setReadyStatus] = useState<boolean>(false)
    const [isBotRunning, setIsBotRunning] = useState<boolean>(false)
    const [startBot, setStartBot] = useState<boolean>(false)
    const [stopBot, setStopBot] = useState<boolean>(false)
    const [refreshAlert, setRefreshAlert] = useState<boolean>(false)

    const [settings, setSettings] = useState<Settings>(defaultSettings)

    const providerValues: IProviderProps = {
        readyStatus,
        setReadyStatus,
        isBotRunning,
        setIsBotRunning,
        startBot,
        setStartBot,
        stopBot,
        setStopBot,
        refreshAlert,
        setRefreshAlert,
        settings,
        setSettings,
    }

    return <BotStateContext.Provider value={providerValues}>{children}</BotStateContext.Provider>
}
