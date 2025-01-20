
import { useBackend } from "@/services/backend";
import { Plant } from "@/types/rest";
import { Autocomplete, CircularProgress, TextField } from "@mui/material";

interface Props {
    plant: Plant | null;
    onPlantationChange: (newPlant: Plant | null) => void;
}
export const PlantChooser: React.FC<Props> = ({ onPlantationChange, plant }) => {
    const { data: plantsRes, isLoading } = useBackend<{ plants: Plant[] }>("/api/plants");
    const plants = plantsRes?.plants;
    return (
        <>
            <Autocomplete
                sx={{float: "right"}}
                options={plants ?? []}
                isOptionEqualToValue={(option, value) => option.uuid === value.uuid}
                value={plant}
                onChange={(_, val) => onPlantationChange(val)}
                getOptionLabel={(option) => option.name}
                loading={isLoading}
                renderInput={(params) => <TextField
                    {...params}
                    label="Roślina"
                    slotProps={{
                      input: {
                        ...params.InputProps,
                        endAdornment: (
                          <>
                            {isLoading ? <CircularProgress color="inherit" size={20} /> : null}
                            {params.InputProps.endAdornment}
                          </>
                        ),
                      },
                    }}
                  />}
            />
        </>
    );
};
