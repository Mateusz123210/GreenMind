export interface Plant {
    uuid: string;
    name: string;
    // description: string;
}

export interface PlantConfig {
    comments: string;
    name: string;
    min_temperature: number,
    opt_temperature: number,
    max_temperature: number,
    min_moisture: number,
    opt_moisture: number,
    max_moisture: number,
    min_illuminance: number,
    opt_illuminance: number,
    max_illuminance: number
}

export type DerangedStatistic = {"Average plant conditions by days": Array<[string, number, number, number]>}