package file

import (
	"github.com/ARXNDEV/glass-fence/server/pkg/types"
)

type MemberEntry struct {
	Password string              `json:"password"`
	Profile  types.MemberProfile `json:"profile"`
}

type Config struct {
	Path string
	Hash bool
}
