import { useBackend } from "@/services/backend";
import { Plantation } from "@/types/rest";
import { Autocomplete, CircularProgress, TextField } from "@mui/material";

interface Props {
    plantation: Plantation | null;
    onPlantationChange: (newPlantation: Plantation | null) => void;
}
export const PlantationChooser: React.FC<Props> = ({ onPlantationChange, plantation }) => {
    const { data: plantationsData, isLoading } = useBackend<{ plantations: Plantation[] }>(
        "/api/plantations"
    );
    const plantations = plantationsData?.plantations;
    return (
        <>
            <Autocomplete
                sx={{float: "right"}}
                options={plantations ?? []}
                isOptionEqualToValue={(option, value) => option.uuid === value.uuid}
                value={plantation}
                onChange={(_, val) => onPlantationChange(val)}
                getOptionLabel={(option) => option.name}
                loading={isLoading}
                renderInput={(params) => <TextField
                    {...params}
                    label="Plantacja"
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
